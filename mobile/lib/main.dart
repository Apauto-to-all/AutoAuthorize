import 'package:flutter/material.dart';
import 'package:workmanager/workmanager.dart';
import 'ui.dart';
import 'notice.dart';
import 'save_and_get.dart';

void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) {
    // 这里是你的后台任务代码
    backgroundRun(); // 后台运行，监测校园网
    return Future.value(true);
  });
}

void main() async {
  //用于确保Flutter的Widgets绑定已经初始化。
  WidgetsFlutterBinding.ensureInitialized();
  // 初始化通知帮助类
  NotificationHelper notificationHelper = NotificationHelper();
  await notificationHelper.initialize();
  // 初始化Workmanager
  Workmanager().initialize(
    callbackDispatcher,
    isInDebugMode: true,
  );
  firstRun(); // 判断是否第一次运行

  runApp(
    const MyApp(),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '自动登入校园网',
      theme: ThemeData(
        colorScheme: const ColorScheme.light(
          onSurface: textColor, // 设置全局字体颜色
        ),
        fontFamily: textFont, // 设置全局字体
      ),
      home: const UiHead(),
    );
  }
}

class UiHead extends StatelessWidget {
  const UiHead({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          '自动登入校园网',
          style: TextStyle(
            fontSize: 30,
            shadows: <Shadow>[
              Shadow(
                offset: Offset(1.0, 1.0),
                blurRadius: 1.0,
                color: Colors.black,
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
    );
  }
}
