import 'package:flutter/material.dart';
import 'ui.dart';
import 'notice.dart';
import 'save_and_get.dart';

void main() async {
  //用于确保Flutter的Widgets绑定已经初始化。
  WidgetsFlutterBinding.ensureInitialized();
  // 初始化通知帮助类
  NotificationHelper notificationHelper = NotificationHelper();
  await notificationHelper.initialize();
  firstRun(); // 判断是否第一次运行

  runApp(
    MaterialApp(
      theme: ThemeData(
        colorScheme: const ColorScheme.light(
          onSurface: textColor, // 设置全局字体颜色
        ),
        fontFamily: textFont, // 设置全局字体
      ),
      home: SafeArea(
        child: Scaffold(
          appBar: AppBar(
            title: const Text(
              '自动登入校园网',
              style: TextStyle(
                fontSize: 30,
                shadows: <Shadow>[
                  Shadow(
                    offset: Offset(1.0, 1.0),
                    blurRadius: 1.0,
                    color: Color.fromARGB(255, 0, 0, 0),
                  ),
                ],
              ),
            ),
            flexibleSpace: Image.asset(
              "images/1.jpg",
              fit: BoxFit.cover,
            ),
          ),
          body: const UiDesign(), // 引入UiDesign
        ),
      ),
    ),
  );
}
