import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'login_ecjtu_wifi.dart';
import 'save_and_get.dart';

class UiDesign extends StatefulWidget {
  const UiDesign({super.key});

  @override
  State<UiDesign> createState() {
    return _UiBody();
  }
}

const textColor = Color.fromRGBO(73, 90, 128, 1);
const textBackgroundColor = Color.fromRGBO(248, 239, 230, 0.8);
const textFont = 'KaiTi'; // 设置字体

class _UiBody extends State<UiDesign> {
  TextEditingController username = TextEditingController(); // 学号输入框控制器
  TextEditingController password = TextEditingController(); // 密码输入框控制器
  String? operator; // 运营商
  String? choiceWifi; // 选择的WiFi
  String isLoginButtonText = '保存账户并验证'; // 是否登入

  @override
  void initState() {
    super.initState();
    showBegin();
  }

  Future<void> showBegin() async {
    String? value = await storage.read(key: 'verifyAccount');
    if (value == '1') {
      setState(() async {
        username.text = await storage.read(key: 'username') ?? '';
        password.text = await storage.read(key: 'password') ?? '';
        operator = await storage.read(key: 'operator');
        isLoginButtonText = '修改账户';
      });
    } else {
      setState(() {
        isLoginButtonText = '保存账户并验证';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('images/2.jpg'), // 你的图片路径
            fit: BoxFit.cover,
          ),
        ),
        child: Padding(
          padding: EdgeInsets.all(MediaQuery.of(context).size.height * 0.01),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              SizedBox(height: MediaQuery.of(context).size.height * 0.02),
              TextField(
                // 学号输入框
                keyboardType: TextInputType.number, // 设置键盘为数字
                inputFormatters: <TextInputFormatter>[
                  FilteringTextInputFormatter.digitsOnly
                ], // 只允许输入数字
                controller: username,
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  labelText: '学号',
                  hintText: '输入学号',
                  filled: true,
                  fillColor: textBackgroundColor, // 设置背景颜色
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.clear),
                    onPressed: username.clear,
                  ),
                ),
              ),
              SizedBox(height: MediaQuery.of(context).size.height * 0.02),
              TextField(
                // 密码输入框
                controller: password, // 控制输入密码
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  labelText: '密码',
                  hintText: '输入密码',
                  filled: true,
                  fillColor: textBackgroundColor, // 设置背景颜色
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.clear),
                    onPressed: password.clear,
                  ),
                ),
                obscureText: true, // 隐藏密码
              ), // 密码输入框结束
              SizedBox(height: MediaQuery.of(context).size.height * 0.02),
              Row(
                // 2下拉框并排
                children: <Widget>[
                  Expanded(
                    child: DropdownButtonFormField<String>(
                      isExpanded: true,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(), labelText: '选择运营商',
                        filled: true,
                        fillColor: textBackgroundColor, // 设置背景颜色
                      ),
                      // 设置默认值
                      value: operator,
                      // 选择回调

                      onChanged: (String? newPosition) {
                        setState(() {
                          operator = newPosition;
                        });
                      },
                      // 传入数组
                      items:
                          <String>['中国电信', '中国联通', '中国移动'].map((String value) {
                        return DropdownMenuItem(
                            value: value, child: Text(value));
                      }).toList(),
                    ), // 下拉框结束
                  ),
                  SizedBox(width: MediaQuery.of(context).size.height * 0.02),
                  Expanded(
                    child: DropdownButtonFormField<String>(
                      isExpanded: true,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: '选择校园网类型',
                        filled: true,
                        fillColor: textBackgroundColor, // 设置背景颜色
                      ),
                      // 设置默认值
                      value: '自动选择',
                      // 选择回调
                      onChanged: (String? newPosition) {
                        setState(() {
                          choiceWifi = newPosition;
                        });
                      },
                      // 传入数组
                      items: <String>['自动选择'].map((String value) {
                        return DropdownMenuItem(
                            value: value, child: Text(value));
                      }).toList(),
                    ), // 网络选择，下拉框结束
                  ),
                ],
              ),
              SizedBox(height: MediaQuery.of(context).size.height * 0.02),
              ElevatedButton(
                // 保存账户并验证，或者修改账户
                onPressed: () async {
                  // 点击事件
                  if (isLoginButtonText == '保存账户并验证') {
                    await saveAndVerify(
                        context, username.text, password.text, operator);
                    showBegin();
                  } else {
                    await initializeData();
                    showMessage(context, "账户已允许修改，修改完成后，请重新进行验证");
                    showBegin();
                  }
                },
                child: Text(
                  isLoginButtonText,
                  style: isLoginButtonText == '保存账户并验证'
                      ? const TextStyle(
                          fontSize: 25,
                          color: textColor,
                          fontFamily: textFont,
                        )
                      : const TextStyle(
                          fontSize: 25,
                          color: Colors.red,
                          fontFamily: textFont,
                        ),
                ),
              ), // 登录按钮结束
              SizedBox(height: MediaQuery.of(context).size.height * 0.02),
              TextButton(
                onPressed: () async {
                  // 按钮点击事件
                  await text(context);
                },
                child: const Text(
                  '说明',
                  style: TextStyle(
                    color: textColor,
                    fontSize: 25,
                    decoration: TextDecoration.underline, // 下划线
                    decorationColor: Colors.deepOrange, // 下划线颜色
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: SizedBox(
        width: 60, // 设置宽度
        height: 60, // 设置高度
        child: FloatingActionButton(
          onPressed: () async {
            // 按钮点击事件
            await linkWifiNow(context); // 登入校园网
          },
          backgroundColor: textBackgroundColor,
          child: const Tooltip(
            message: '点击此按钮立即登入校园网',
            child: Icon(
              Icons.login,
              color: textColor,
            ), // 图标
          ),
        ),
      ),
    );
  }
}
