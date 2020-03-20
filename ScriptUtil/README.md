# 个人专用脚本

## Python 版本 > 3.0
## 环境变量:THUNDER_DIRECTORY

# 插件

- ## CsbToCsd
    >cocostudio csb反编成csd  
    lua版本[csb2csd](https://github.com/DavidFeng/csb2csd)  
    python版本[csb2csd](https://github.com/lyzz0612/csb2csd)

    ### 使用说明
    `thunder to_csd 'csb文件'`

    ### 配置相关
    1. `CSParseBinary.fbs` 是基于`cocos/editor-support/cocostudio/fbs-files/CSParseBinary.fbs`，添加了一些其他结构，使用`flatc -p CSParseBinary.fbs`生成库结构，部分坑需要手动修改

    2. `header_rule.json`和`child_rule.json`是导出csd的规则配置，其中`header_rule.json`是对应csd中类似`<AbstractNodeData Name="room_bg" ActionTag="-1313931908" Tag="1" ...`这样的格式，`child_rule.json`对应`<AnchorPoint ScaleX="0.5" ScaleY="0.5" />`的格式

        1. `header_rule.json` 以Button为例, 
        ```
        配置
        "Button":[
                ["DisplayState", "Displaystate", false, ""],
                ["Scale9Enable", "Scale9Enabled", false, ""],
                ["LeftEage", "CapInsets.X", 0.0, ""],
                ["RightEage", "CapInsets.X", 0.0, ""],
                ["TopEage", "CapInsets.Y", 0.0, ""],
                ["BottomEage", "CapInsets.Y", 0.0, ""],
                ["Scale9OriginX", "CapInsets.X", 0.0, ""],
                ["Scale9OriginY", "CapInsets.Y", 0.0, ""],
                ["Scale9Width", "CapInsets.Width", 0.0, ""],
                ["Scale9Height", "CapInsets.Height", 0.0, ""],
                ["ShadowOffsetX", "ShadowOffsetX", 0.0, ""],
                ["ShadowOffsetY", "ShadowOffsetY", 0.0, ""],
                ["ButtonText", "Text", "", ""],
                ["FontSize", "FontSize", "", ""]
            ],
        ```
        ```
        对应csd结构
        <AbstractNodeData DisplayState="True" Scale9Enable="True" LeftEage="15" RightEage="15" 
           TopEage="11" BottomEage="11" Scale9OriginX="15" Scale9OriginY="11" Scale9Width="1" Scale9Height="9" 
           ShadowOffsetX="2" ShadowOffsetY="-2" ButtonText="Test" FontSize="14">
        ```
        ```
        fbs结构
           table ButtonOptions
           {
               widgetOptions:WidgetOptions;
        
               normalData:ResourceData;
               pressedData:ResourceData;
               disabledData:ResourceData;
               fontResource:ResourceData;
               text:string;
               fontName:string;
               fontSize:int;
               textColor:Color;
               capInsets:CapInsets;
               scale9Size:FlatSize;
               scale9Enabled:bool;
               displaystate:bool;
        
               outlineEnabled:bool = false;
               outlineColor:Color;
               outlineSize:int = 1;
               shadowEnabled:bool = false;
               shadowColor:Color;
               shadowOffsetX:float = 2;
               shadowOffsetY:float = -2;
               shadowBlurRadius:int;
               isLocalized:bool = false;
           }
        ```
        `["Scale9OriginY", "CapInsets.Y", 0.0, ""]`第一个为csd的字段名，第二个为根据fbs取值的字段路径, 第三个为默认值，等于默认值的将不写到csd中，第四个为重命名，如`["ProgressType", "Direction", 0, "0=Left_To_Right,1=Right_To_Left"]`就是值为0时，写入csd的是Left_To_Right，1时写入Right_To_Left

        2. `child_rule.json` 跟2.1类似
   
         `<Size X="100" Y="100" />`
        ``` fbs
        struct FlatSize
        {
           width:float;
           height:float;
        }
        ```
        `["Size", "Size", "X=Width,Y=Height", ""],` 第一个为csd的字段名，第二个为根据fbs取值的字段路径, 第三个为重命名，即将width的值以键X写入csd，第四个为特殊标记，不赋值的时候会按照fbs的字段格式导出，特殊值目前只有ImageData,代表这是文件路径格式
