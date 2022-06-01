#!/usr/bin/env node
import {$, cd, chalk} from 'zx'
import {createObjectCsvWriter} from 'csv-writer'
/*
 * Usage:
 * sancov_utils.mjs <path to experiment-data>
 *
 * Requirements:
 * - sancov
 * - node 16+
 * - run npm install in this directory
 * - set ALL_SNAPSHOTS
 */
'use strict';
$.verbose = false

// if false do only use last snapshot, i.e. one snapshot per trial
const ALL_SNAPSHOTS = true
const DEL_TMP_DIR = false

if (process.argv.length != 3) {
    console.log("needs path to experiment, e.g. /home/b/bdata-unsync/ast-fuzz/experiment-data/exp-2022-05-28-20-02-46'")
    process.exit(0)
}

const BM_DIR = process.argv[2]
const pwd = (await $`pwd`).stdout.trim()

// Tmp directory
const TMP_ROOT = pwd + '/sancov_util_tmp'
if (DEL_TMP_DIR) {
    info(`Deleting temp dir ${TMP_ROOT}`)
    await $`rm -rf ${TMP_ROOT}`
}
await $`mkdir -p ${TMP_ROOT}`

// data directory
let exp = await base(BM_DIR)
const RES_DIR = pwd + '/sancov_util_results/' + exp
info(`Creating result dir ${RES_DIR}`)
await $`mkdir -p ${RES_DIR}`

let csvData = []
const csvPath = RES_DIR + '/sancov_out.csv'


let headersFuzzbench = ['id', 'git_hash', 'experiment_filestore', 'experiment', 'fuzzer', 'benchmark', 'time_started',
    'time_ended', 'trial_id', 'time', 'edges_covered', 'fuzzer_stats', 'crash_key', 'bugs_covered']

let headersSancov = ['corpusNr', 'sancov_file']

let headers = []
headersFuzzbench.concat(headersSancov).forEach(t => headers.push({
    id: t,
    title: t
}))
const csvWriter = createObjectCsvWriter({
    path: csvPath,
    header: headers
});

await main(BM_DIR)

csvWriter
    .writeRecords(csvData)
    .then(() => console.log('The CSV file was written successfully', csvPath));

async function main(dir) {
    let covBinary = await extractCovBinary(dir)
    let benchmarks = await getFuzzerBmPairs(dir)
    for (let b of benchmarks) {
        let trials = await getTrials(dir, b)
        for (let t of trials) {
            let corpuses = await getCorpusesForTrial(t)

            if (ALL_SNAPSHOTS) {
                for (let c of corpuses) {
                    await handleEntry(covBinary, dir, b, t, c)
                }
            } else {
                // Use only last corpus
                let _cx = corpuses.filter(c => c.endsWith("tar.gz")).sort()
                let c = _cx[_cx.length - 1]
                await handleEntry(covBinary, dir, b, t, c)
            }
        }
    }
}

async function handleEntry(covBinary,
                           experimentPath,
                           benchmarkPath,
                           trialPath,
                           corpusTarPath) {

    if (!corpusTarPath.endsWith("tar.gz")) {
        console.log(`skipping ${corpusTarPath}`)
        return
    }

    let corpusPath = await extractCorpus(corpusTarPath)
    let covFile = await coverageRun(covBinary, corpusPath)
    let trialNr = parseInt((await base(trialPath)).replace('trial-', ''))
    let corpusNr = parseInt((await (base(corpusTarPath))).replace('corpus-archive-', '').replace('.tar.gz', ''))

    let expName = await (base(experimentPath))
    let benchFuzzerName = await base(benchmarkPath) // <benchmark>_fuzzer
    let trialName = await base(trialPath)
    let corpusName = await base(corpusPath)
    let edges = await sancovReachedEdges(covFile)
    let benchName = await extractBenchmarkName(experimentPath)
    let fuzzer = benchFuzzerName.replace(benchName + '-', '')

    let finalName = RES_DIR + `/sancov__${expName}__${benchName}__${fuzzer}__${trialName}__${corpusNr}.sancov`
    await $`cp -rf ${covFile} ${finalName}`

    info(`Benchmark ${benchName}, fuzzer: ${fuzzer}, trial ${trialNr}, corpus ${corpusNr} got ${edges} edges`)

    // same format as fuzzbench data.csv and some extra stuff
    let entry = {
        'id': 0,
        'git_hash': 0,
        'experiment_filestore': '/not/relevant',
        'experiment': expName,
        'fuzzer': fuzzer,
        'benchmark': benchName,
        'time_started': '2022-05-27 04:39:42',
        'time_ended': '2022-05-27 08:49:44',
        'trial_id': trialNr,
        'time': 15 * 60 * corpusNr, // snapshot frequence is 15 mins
        'edges_covered': edges,
        'fuzzer_stats': '',
        'crash_key': '',
        'bugs_covered': 0,
        // sancov
        'corpusNr': corpusNr,
        'sancov_file': finalName
    }
    csvData.push(entry)
}

async function sancovReachedEdges(sancovFile) {
    return (await $`sancov -print ${sancovFile}`).stdout.trim().split(/\r?\n/).length
}

async function base(dir) {
    return (await $`basename -- ${dir}`).stdout.trim()
}

async function extractCorpus(corpusDir) {
    const tmpDir = (await $`mktemp -d  --tmpdir=${TMP_ROOT}`).stdout.trim()
    try {
        await $`tar -xf ${corpusDir} -C ${tmpDir}`
    } catch (exception) {
        console.log(corpusDir)
        console.log(exception)
    }
    return tmpDir + '/corpus/default/queue'
}

async function extractCovBinary(bmDir) {
    const tmpDir = (await $`mktemp -d --tmpdir=${TMP_ROOT}`).stdout.trim()
    cd(tmpDir)
    await $`tar -xf ${bmDir}/coverage-binaries/* -C ${tmpDir}`
    cd(tmpDir)
    let binary = (await $`find . -maxdepth 1 -type f -executable -print`).stdout.trim().replace('./', '')
    return tmpDir + '/' + binary
}

async function coverageRun(binary, corpusDir) {
    const tmpDir = (await $`mktemp -d  --tmpdir=${TMP_ROOT}`).stdout.trim()
    // await $`UBSAN_OPTIONS=allocator_release_to_os_interval_ms=500:handle_abort=2:handle_segv=2:handle_sigbus=2:handle_sigfpe=2:handle_sigill=2:print_stacktrace=1:symbolize=1:symbolize_inline_frames=0  ASAN_OPTIONS=alloc_dealloc_mismatch=0:allocator_may_return_null=1:allocator_release_to_os_interval_ms=500:allow_user_segv_handler=0:check_malloc_usable_size=0:detect_leaks=1:detect_odr_violation=0:detect_stack_use_after_return=1:fast_unwind_on_fatal=0:handle_abort=2:handle_segv=2:handle_sigbus=2:handle_sigfpe=2:handle_sigill=2:max_uar_stack_size_log=16:quarantine_size_mb=64:strict_memcmp=1:symbolize=1:symbolize_inline_frames=0:coverage=1:coverage_dir=${tmpDir} ${binary} ${corpusDir}`
    await $`ASAN_OPTIONS=coverage=1:coverage_dir=${tmpDir} ${binary} ${corpusDir}`
    let covFile = await getDirContent(tmpDir, 'f')
    return covFile
}

async function getDirContent(dir, type = 'd') {
    cd(dir)
    let res = (await $`find . -maxdepth 1 -type ${type} -print`).stdout.trim().split(/\r?\n/)
        .filter(el => el != "./")
        .filter(el => el != ".")
        .map(el => el.replace('./', ''))
        .map(el => dir + '/' + el)
    res.sort()
    return res

}

async function getCorpusesForTrial(trialDir) {
    return await getDirContent(trialDir + '/corpus', 'f')
}

async function getTrials(bmDir, fuzzerBmPair) {
    return await getDirContent(fuzzerBmPair)
}

async function getFuzzerBmPairs(bmDir) {
    const dir = bmDir + '/experiment-folders'
    return await getDirContent(dir)
}

function info(...msg) {
    console.log(chalk.blue('[+] ' + msg))
}

async function extractBenchmarkName(bmDir) {
    // coverage-build: coverage-binaries/coverage-build-vorbis-2017-12-11.tar.gz -> vorbis-2017-12-11
    const dir = bmDir + '/coverage-binaries'
    let entry = (await getDirContent(dir, 'f'))[0]
    entry = await (base(entry))
    return entry.replace('.tar.gz', '').replace('coverage-build-', '')
}