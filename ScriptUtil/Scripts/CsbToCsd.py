#!/usr/bin/python
# -*- coding: utf-8 -*-
import thunder
import flatbuffers as Parser
import string
import random
import json
from Attribute import PluginDesAttribute
from TUtils import *

COCOS_ENGINE_VERSION = "3.10.0.0"


@PluginDesAttribute(name="to_csd", description=getCurString(u"[将csb文件转换为csd]"))
class CsbToCsdPlugin(thunder.Plugin):
    HeaderRules = None
    ChildRules = None

    def __init__(self):
        super(CsbToCsdPlugin, self).__init__()
        self.filePath = None
        self.csdPath = None
        self.csbPath = None
        self.writeTarget = None  # 写入文件对象

    def read_config(self):
        with open(os.path.join(self.scriptPath, "Res/header_rule.json"), "r") as fileObj:
            CsbToCsdPlugin.HeaderRules = json.load(fileObj)
            fileObj.close()
        with open(os.path.join(self.scriptPath, "Res/child_rule.json"), "r") as fileObj:
            CsbToCsdPlugin.ChildRules = json.load(fileObj)
            fileObj.close()

        if CsbToCsdPlugin.HeaderRules is None or CsbToCsdPlugin.ChildRules is None:
            return False

        return True

    def check_custom_options(self, args):
        self.filePath = args.file

    def parse_args(self, parser):
        super(CsbToCsdPlugin, self).parse_args(parser)
        parser.add_argument(dest='file', help='csb path')

    def run(self, argv):
        super(CsbToCsdPlugin, self).run(argv)
        # 初始化路径
        self.csdPath = os.path.join(self.currPath, "csd")
        self.csbPath = os.path.join(self.currPath, self.filePath)

        # 加载配置文件 并初始化参数
        success = self.read_config()
        if not success:
            return

        if not os.path.exists(self.csdPath):
            os.mkdir(self.csdPath)

        if os.path.isdir(self.csbPath):
            for f in os.listdir(self.csbPath):
                if f.rfind(".csb") > 0:
                    print(os.path.join(self.csbPath, f))
        else:
            self.start_convert(self.csbPath)

    def start_convert(self, csbFile):
        _, fileName = os.path.split(csbFile)
        groupName, suffix = os.path.splitext(fileName)
        if suffix != ".csb":
            print(getCurString(u"请选择Csb文件"))
            return

        with open(csbFile, "rb") as fileObj:
            buf = fileObj.read()
            fileObj.close()

            buf = bytearray(buf)
            csparsebinary = Parser.CSParseBinary.GetRootAsCSParseBinary(buf, 0)

            self.writeTarget = os.path.join(self.csdPath, groupName + ".csd")
            if os.path.exists(self.writeTarget):
                os.remove(self.writeTarget)

            nodeTree = csparsebinary.NodeTree()

            self.write_header(groupName)
            self.write_action(csparsebinary.Action())
            self.write_animation(csparsebinary)
            self.write_root_node(nodeTree)
            self.recursion_convert_tree(nodeTree)
            self.write_footer()

        print(getCurString(u"Csd [%s] 转化完成") % groupName)

    def write_file(self, text):
        if not self.writeTarget:
            return
        with open(self.writeTarget, "a") as fileObj:
            fileObj.write(text)
            fileObj.close()

    def write_header(self, groupName):
        randomId = random.sample(string.ascii_lowercase + "-" + string.digits, 36)
        randomId = "".join(randomId)
        text = ''
        text = text + '<GameFile>\n'
        text = text + '  <PropertyGroup Name="%s" Type="Layer" ID="%s" Version="%s" />\n' % (groupName, randomId, COCOS_ENGINE_VERSION)
        text = text + '  <Content ctype="GameProjectContent">\n'
        text = text + '    <Content>\n'
        self.write_file(text)

    def write_footer(self):
        text = ''
        text = text + '    </Content>\n'
        text = text + '  </Content>\n'
        text = text + '</GameFile>\n'
        self.write_file(text)

    def get_image_option(self, childKey, resourceData):
        fileType = "Default"
        if resourceData.ResourceType() == 0:
            fileType = "Normal"
        elif resourceData.ResourceType() == 1:
            fileType = "PlistSubImage"
        path = bytes.decode(resourceData.Path())
        plistFile = bytes.decode(resourceData.PlistFile())
        if path == "" and plistFile == "":
            return '  <%s />\n' % childKey
        text = '  <%s Type="%s" Path="%s" Plist="%s" />\n' % (childKey, fileType, path, plistFile)
        return text

    def get_easing_text(self, easingData):
        if not easingData:
            return ""
        easingType = easingData.Type()
        if easingType == -1:
            return ""
        else:
            return '            <EasingData Type="%d" />\n' % (easingType)

    def get_frame_text(self, frameData, property):
        text = ""
        if property == "VisibleForFrame":
            realFrame = frameData.BoolFrame()
            text = text + '          <BoolFrame FrameIndex="%d" Tween="%s" Value="%s" />\n' % (
                realFrame.FrameIndex(), realFrame.Tween(), realFrame.Value())

        elif property == "Position":
            realFrame = frameData.PointFrame()
            text = text + '          <PointFrame FrameIndex="%d" X="%f" Y="%f">\n' % (
                realFrame.FrameIndex(), realFrame.Position().X(), realFrame.Position().Y())
            text = text + self.get_easing_text(realFrame.EasingData())
            text = text + '          </PointFrame>\n'

        elif property == "Scale":
            realFrame = frameData.ScaleFrame()
            text = text + '          <ScaleFrame FrameIndex="%d" X="%f" Y="%f">\n' % (
                realFrame.FrameIndex(), realFrame.Scale().ScaleX(), realFrame.Scale().ScaleX())
            text = text + self.get_easing_text(realFrame.EasingData())
            text = text + '          </ScaleFrame>\n'

        elif property == "RotationSkew":
            realFrame = frameData.ScaleFrame()
            text = text + '          <ScaleFrame FrameIndex="%d" X="%f" Y="%f">\n' % (
                realFrame.FrameIndex(), realFrame.Scale().ScaleX(), realFrame.Scale().ScaleX())
            text = text + self.get_easing_text(realFrame.EasingData())
            text = text + '          </ScaleFrame>\n'

        elif property == "CColor":
            realFrame = frameData.ColorFrame()
            colorData = realFrame.Color()
            text = text + '          <ColorFrame FrameIndex="%d" Alpha="%d">\n' % (realFrame.FrameIndex(), colorData.A())
            text = text + '            <Color A="%d" R="%d" G="%d" B="%d" />' % (colorData.A(), colorData.R(), colorData.G(), colorData.B())
            text = text + '          </ColorFrame>\n'

        elif property == "FileData":
            realFrame = frameData.TextureFrame()
            text = text + '          <TextureFrame FrameIndex="%d" Tween="%s">\n' % (realFrame.FrameIndex(), realFrame.Tween())
            text = text + '          ' + self.get_image_option("TextureFile", realFrame.TextureFile())
            text = text + '          </TextureFrame>\n'

        elif property == "FrameEvent":
            realFrame = frameData.EventFrame()
            text = text + '          <EventFrame FrameIndex="%d" Value="%s">\n' % (realFrame.FrameIndex(), realFrame.Value())
            text = text + '          </EventFrame>\n'

        elif property == "Alpha":
            realFrame = frameData.IntFrame()
            text = text + '          <IntFrame FrameIndex="%d" Value="%d">\n' % (realFrame.FrameIndex(), realFrame.Value())
            text = text + '          </IntFrame>\n'

        elif property == "AnchorPoint":
            realFrame = frameData.ScaleFrame()
            text = text + '          <ScaleFrame FrameIndex="%d" X="%f" Y="%f">\n' % (
                realFrame.FrameIndex(), realFrame.Scale().ScaleX(), realFrame.Scale().ScaleX())
            text = text + self.get_easing_text(realFrame.EasingData())
            text = text + '          </ScaleFrame>\n'

        elif property == "ZOrder":
            realFrame = frameData.IntFrame()
            text = text + '          <IntFrame FrameIndex="%d" Value="%d">\n' % (realFrame.FrameIndex(), realFrame.Value())
            text = text + '          </IntFrame>\n'

        elif property == "ActionValue":
            realFrame = frameData.InnerActionFrame()
        # todo
        elif property == "BlendFunc":
            realFrame = frameData.BlendFrame()
            text = text + '          <BlendFuncFrame FrameIndex="%d" Src="%d" Dst="%d">\n' % (
                realFrame.FrameIndex(), realFrame.BlendFunc().Src(), realFrame.BlendFunc().Dst())
            text = text + '          </BlendFuncFrame>\n'
        return text

    def get_timeline(self, timeLineData):
        property = timeLineData.Property()
        text = '        <Timeline ActionTag="%d" Property="%s">\n' % (timeLineData.ActionTag(), timeLineData.Property())
        frameNum = timeLineData.FramesLength()
        for i in range(frameNum):
            frameData = timeLineData.Frames(i)
            text = text + self.get_frame_text(frameData, property)
        text = text + '        </Timeline>\n'
        return text

    def write_action(self, actionData):
        duration = actionData.Duration()
        speed = actionData.Speed()
        timelineNum = actionData.TimeLinesLength()
        text = '      <Animation Duration="%d" Speed="%f">\n' % (duration, speed)
        for i in range(timelineNum):
            timeLineData = actionData.TimeLines(i)
            text = text + self.get_timeline(timeLineData)

        text = text + '      </Animation>\n'
        self.write_file(text)

    def write_animation(self, parseData):
        animationNum = parseData.AnimationListLength()
        if animationNum == 0:
            return
        text = '      <AnimationList>\n'
        for i in range(animationNum):
            animationData = parseData.AnimationList(i)
            text = text + '        <AnimationInfo Name="%s" StartIndex="%d" EndIndex="%d" />\n' % (
                animationData.Name(), animationData.StartIndex(), animationData.EndIndex())
        text = '      </AnimationList>\n'
        self.write_file(text)

    def write_root_node(self, nodeTree):
        widgetOption = nodeTree.Options().Data()
        widgetSize = widgetOption.Size()
        if not widgetSize:
            boneOption = Parser.BoneNodeOptions()
            boneOption._tab = widgetOption._tab
            widgetOption = boneOption.NodeOptions()

        widgetSize = widgetOption.Size()
        widgetName = bytes.decode(widgetOption.Name())
        text = ''
        nodeObject = {
            "Node": "GameNodeObjectData",
            "Scene": "GameNodeObjectData",
            "Layer": "GameLayerObjectData",
            "Skeleton": "SkeletonNodeObjectData",
        }
        text = text + '      <ObjectData Name="%s" ctype="%s">\n' % (widgetName, nodeObject[widgetName])
        text = text + '        <Size X="%f" Y="%f" />\n' % (widgetSize.Width(), widgetSize.Height())
        self.write_file(text)

    def get_real_option(self, className, optionData):
        realOption = None
        optionClassName = className + "Options"
        try:
            optionClass = getattr(Parser, optionClassName)
        except Exception as e:
            print("error no match className: " + optionClassName)
            return

        if optionClass:
            realOption = optionClass()

        if realOption:
            realOption._tab = optionData.Data()._tab
            return realOption
        else:
            return optionData

    def get_header_option(self, optionData, optionKey, valuePath, defaultValue="", replaceInfo=""):
        valueList = valuePath.split(".")
        parentValue = optionData
        for path in valueList:
            if not parentValue:
                return ""
            func = getattr(parentValue, path)
            if not func:
                return ""
            parentValue = func()
        result = bytes.decode(parentValue) if isinstance(parentValue, bytes) else str(parentValue)
        if result.upper() == str(defaultValue).upper():
            return ""
        result = result.replace("\n", "&#xA;")
        if result.find(".") != -1:
            result = result.rstrip("0")
            result = result.rstrip(".")

        renameDict = {}
        if replaceInfo != "":
            renameList = replaceInfo.split(",")
            for renameText in renameList:
                kvList = renameText.split("=")
                renameDict[kvList[0]] = kvList[1]
        if result in renameDict:
            result = renameDict[result]
        text = '%s="%s" ' % (optionKey, result)

        # scale9sprite special
        # if optionKey == "Scale9Enabled":
        # # if optionKey == "Scale9Enable" and result == "True":
        # 	text = text + getHeaderOption(optionData, "Scale9OriginX", "CapInsets.X")
        # 	text = text + getHeaderOption(optionData, "Scale9OriginY", "CapInsets.Y")
        # 	text = text + getHeaderOption(optionData, "Scale9Width", "CapInsets.Width")
        # 	text = text + getHeaderOption(optionData, "Scale9Height", "CapInsets.Height")
        return text

    def get_default_optionHeader(self, widgetOption, tab):
        text = tab + '<AbstractNodeData '
        DefaultRules = CsbToCsdPlugin.HeaderRules["Default"]
        for ruleOption in DefaultRules:
            text = text + self.get_header_option(widgetOption, ruleOption[0], ruleOption[1], ruleOption[2])
        return text

    def write_optionHeader(self, optionData, widgetOption, className, tab):
        text = self.get_default_optionHeader(widgetOption, tab)
        if className in CsbToCsdPlugin.HeaderRules:
            ClassRules = CsbToCsdPlugin.HeaderRules[className]
            for ruleOption in ClassRules:
                text = text + self.get_header_option(optionData, ruleOption[0], ruleOption[1], ruleOption[2], ruleOption[3])
        text = text + 'ctype="%sObjectData">\n' % className
        self.write_file(text)

    def get_child_property(self, optionData, optionKey, valuePath, renameProperty="", specialType=""):
        valueList = valuePath.split(".")
        parentValue = optionData
        for path in valueList:
            func = getattr(parentValue, path)
            if not func:
                return ""
            parentValue = func()

        if specialType == "ImageData":
            return self.get_image_option(optionKey, parentValue)

        funcList = dir(parentValue)
        validFuncList = []
        for funcName in funcList:
            if funcName.startswith("_"):
                continue
            if funcName == "Init" or funcName.startswith("GetRoot"):
                continue
            validFuncList.append(funcName)
        renameDict = {}
        if renameProperty != "":
            renameList = renameProperty.split(",")
            for renameText in renameList:
                kvList = renameText.split("=")
                renameDict[kvList[1]] = kvList[0]
        text = '  <%s ' % optionKey
        for funcName in validFuncList:
            func = getattr(parentValue, funcName)
            result = func()
            keyValue = funcName
            if funcName in renameDict:
                keyValue = renameDict[funcName]
            if isinstance(result, float) and result > 1.1:
                result = int(result)
            text = text + '%s="%s" ' % (keyValue, str(result))
        text = text + "/>\n"
        return text

    def get_default_option_child(self, widgetOption, tab):
        DefaultRules = CsbToCsdPlugin.ChildRules["Default"]
        text = ""
        for childRule in DefaultRules:
            text = text + tab + self.get_child_property(widgetOption, childRule[0], childRule[1], childRule[2], childRule[3])
        return text

    def write_child_option(self, realOption, widgetOption, className, tab):
        text = self.get_default_option_child(widgetOption, tab)

        if className in CsbToCsdPlugin.ChildRules:
            ClassRules = CsbToCsdPlugin.ChildRules[className]
            for childRule in ClassRules:
                text = text + tab + self.get_child_property(realOption, childRule[0], childRule[1], childRule[2], childRule[3])
        self.write_file(text)

    def write_option(self, nodeTree, tab):
        optionData = nodeTree.Options()
        className = str(nodeTree.Classname(), encoding="utf-8")
        realOption = self.get_real_option(className, optionData)
        if not realOption:
            defaultText = tab + '<AbstractNodeData ctype="%seObjectData">\n' % (className)
            self.write_file(defaultText)
            return
        try:
            widgetOption = realOption.WidgetOptions()
        except:
            widgetOption = realOption.NodeOptions()

        self.write_optionHeader(realOption, widgetOption, className, tab)
        self.write_child_option(realOption, widgetOption, className, tab)

    def recursion_convert_tree(self, nodeTree, level=0):
        baseTab = '      ' + "    " * level
        if level > 0:
            self.write_option(nodeTree, baseTab)

        childNum = nodeTree.ChildrenLength()
        if childNum > 0:
            self.write_file(baseTab + '  <Children>\n')
            for i in range(childNum):
                child = nodeTree.Children(i)
                self.recursion_convert_tree(child, level + 1)
            self.write_file(baseTab + '  </Children>\n')
        if level > 0:
            self.write_file(baseTab + '</AbstractNodeData>\n')
        else:
            self.write_file(baseTab + '</ObjectData>\n')
