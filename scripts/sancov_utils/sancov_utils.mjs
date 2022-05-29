#!/usr/bin/env zx
'use strict';

$.verbose = false


const BM_DIR = '/home/b/bdata-unsync/ast-fuzz/experiment-data/exp-2022-05-28-20-02-46'

const pwd = (await $`pwd`).stdout.trim()
const TMP_ROOT = pwd + '/sancov_util_tmp'
await $`rm -rf ${TMP_ROOT}`
await $`mkdir -p ${TMP_ROOT}`

const RES_DIR = pwd + '/sancov_util_results'
await $`mkdir -p ${RES_DIR}`

let dir = BM_DIR
await main(dir)


async function main(dir) {
    let covBinary = await extractCovBinary(dir)
    let benchmarks = await getFuzzerBmPairs(dir)
    for(let b of benchmarks) {
        let trials = await getTrials(dir, b)
        for(let t of trials) {
            let corpuses = await getCorpusesForTrial(t)
            for(let c of corpuses) {
                if (!c.endsWith("tar.gz")) {
                    console.log(`skipping ${c}`)
                    continue
                }
                let corpusPath = await extractCorpus(c)
                let covFile = await coverageRun(covBinary, corpusPath)

                let trialNr = parseInt((await base(t)).replace('trial-', ''))
                let corpusNr = parseInt((await(base(c))).replace('corpus-archive-', '').replace('.tar.gz', ''))

                await handleEntry(dir, b, t, trialNr, corpusPath, corpusNr, covFile)
            }
        }
    }
}

async function handleEntry(experimentPath,
                           benchmarkPath,
                           trialPath,
                           trialNr,
                           corpusPath,
                           corpusNr,
                           coverageFile) {


    let expName = await(base (experimentPath))
    let benchName = await base(benchmarkPath)
    let trialName = await base(trialPath)
    let corpusName = await base(corpusPath)
    let covNamee = await base(coverageFile)
    let edges = await sancovReachedEdges(coverageFile)

    let finalName = RES_DIR  + `/sancov__${expName}__${benchName}__${trialName}__${corpusNr}.sancov`
    await $`cp -rf ${coverageFile} ${finalName}`

    console.log(edges, 'for ' + finalName)
}

async function sancovReachedEdges(sancovFile) {
    return (await $`sancov -print ${sancovFile}`).stdout.trim().split(/\r?\n/).length
}

async function base(dir) {
    return (await $`basename -- ${dir}`).stdout.trim()
}

async function extractCorpus(corpusDir) {
    const tmpDir = (await $`mktemp -d  --tmpdir=${TMP_ROOT}`).stdout.trim()
    try{
        await $`tar -xf ${corpusDir} -C ${tmpDir}`
    }
    catch(exception) {
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
    let binary=(await $`find . -maxdepth 1 -type f -executable -print`).stdout.trim().replace('./', '')
    return tmpDir + '/' + binary
}


async function coverageRun(binary, corpusDir) {
    const tmpDir = (await $`mktemp -d  --tmpdir=${TMP_ROOT}`).stdout.trim()
    await $`ASAN_OPTIONS=coverage=1:coverage_dir=${tmpDir} ${binary} ${corpusDir}`
    let covFile = await getDirContent(tmpDir, 'f')
    return covFile
}


async function getDirContent(dir, type='d') {
    cd(dir)
    let res = (await $`find . -maxdepth 1 -type ${type} -print`).stdout.trim().split(/\r?\n/)
                                                                .filter(el => el != "./")
                                                                .filter(el => el!= ".")
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
