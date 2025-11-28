import sys
import os
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om


def maya_useNewAPI():
    pass


def syntaxCreator():
    syntax = om.MSyntax()
    syntax.addFlag('sn', 'scriptNode', om.MSyntax.kString)
    syntax.addFlag('sj', 'scriptJob', om.MSyntax.kLong)
    return syntax


class CleanPuTianTongQing(om.MPxCommand):
    kPluginCmdName = "cleanPuTianTongQing"
    callbackIdList = []
    procList = [
        'autoUpdatcAttrEd',
        'autoUpdateAttrEd_SelectSystem',
        'UI_Mel_Configuration_think',
        'UI_Mel_Configuration_think_a',
        'UI_Mel_Configuration_think_b',
        'autoUpdatoAttrEnd'
    ]

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return CleanPuTianTongQing()

    def doIt(self, args):
        argData = om.MArgParser(self.syntax(), args)

        if argData.isFlagSet('sn'):
            flagValue = argData.flagArgumentString('sn', 0)
            if cmds.objExists(flagValue):
                cmds.delete(flagValue)
                print 'delete PuTianTongQing scrpitNode.'

        elif argData.isFlagSet('sj'):
            flagValue = argData.flagArgumentInt('sj', 0)
            if cmds.scriptJob(exists=flagValue):
                cmds.scriptJob(kill=flagValue, force=1)
                print 'kill PuTianTongQing scrpitJob.'

    @staticmethod
    def overrideProc():
        procNum = 0
        for proc in CleanPuTianTongQing.procList:
            if mel.eval('whatIs("%s")' % proc) != 'Unknown':
                mel.eval('global proc %s(){}' % proc)
                procNum += 1
        if procNum:
            print 'override PuTianTongQing proc.'

    @staticmethod
    def killScriptJob():
        for job in cmds.scriptJob(listJobs=1):
            if 'autoUpdatoAttrEnd' in job or 'leukocyte.antivirus' in job:
                jobId = job.split(':')[0]
                cmds.evalDeferred('cmds.cleanPuTianTongQing(sj=%s)' % jobId)

    @staticmethod
    def deleteScriptNode():
        for node in cmds.ls(type='script'):
            if 'vaccine_gene' in node:
                cmds.lockNode(node,l = 0)
                cmds.delete(node)
                _maya_dir = cmds.internalVar(userAppDir=True) + 'scripts'
                vaccine = _maya_dir + '/vaccine.py'
                vaccine_pyc = _maya_dir + '/vaccine.pyc'
                usersetup = _maya_dir + '/userSetup.py'
                if os.path.exists(vaccine):
                    os.remove(vaccine)
                if os.path.exists(vaccine_pyc):
                    os.remove(vaccine_pyc)
                if os.path.exists(usersetup):
                    os.remove(usersetup)
                continue
            scriptdata = cmds.scriptNode(node, q=1, bs=1)
            if not scriptdata:
                continue
            if 'MayaMelUIConfigurationFile' in node:
                if 'PuTianTongQing' in scriptdata or 'fuck_All_U' in scriptdata:
                    cmds.scriptNode(node, e=1, bs='')
                    cmds.evalDeferred('cmds.cleanPuTianTongQing(sn="%s")' % node)

            if 'uiConfigurationScriptNode' in node:
                if 'look' in scriptdata:
                    cmds.scriptNode(node, e=1, bs='')
                    cmds.evalDeferred('cmds.cleanPuTianTongQing(sn="%s")' % node)
    @staticmethod
    def procCallback(procName, procID, isProcEntry, procType, clientData):
        if procName in CleanPuTianTongQing.procList:
            CleanPuTianTongQing.overrideProc()
            CleanPuTianTongQing.killScriptJob()
            CleanPuTianTongQing.deleteScriptNode()

    @staticmethod
    def afterLoadCallback(clientData):
        CleanPuTianTongQing.overrideProc()
        CleanPuTianTongQing.killScriptJob()
        CleanPuTianTongQing.deleteScriptNode()

    @staticmethod
    def beforeSaveCallback(clientData):
        CleanPuTianTongQing.killScriptJob()
        CleanPuTianTongQing.deleteScriptNode()


# Initialize the plug-in
def initializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.registerCommand(
            CleanPuTianTongQing.kPluginCmdName, CleanPuTianTongQing.creator, syntaxCreator
        )
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % CleanPuTianTongQing.kPluginCmdName
        )
        raise

    CleanPuTianTongQing.callbackIdList.append(
        om.MCommandMessage.addProcCallback(CleanPuTianTongQing.procCallback)
    )
    CleanPuTianTongQing.callbackIdList.append(
        om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSceneReadAndRecordEdits, CleanPuTianTongQing.afterLoadCallback)
    )
    CleanPuTianTongQing.callbackIdList.append(
        om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave, CleanPuTianTongQing.beforeSaveCallback)
    )
    CleanPuTianTongQing.callbackIdList.append(
        om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeExport, CleanPuTianTongQing.beforeSaveCallback)
    )


# Uninitialize the plug-in
def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    for id in CleanPuTianTongQing.callbackIdList:
        om.MMessage.removeCallback(id)

    try:
        plugin.deregisterCommand(CleanPuTianTongQing.kPluginCmdName)
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % CleanPuTianTongQing.kPluginCmdName
        )
        raise
