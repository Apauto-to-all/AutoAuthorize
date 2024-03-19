import 'package:network_info_plus/network_info_plus.dart'; // 导入network_info_plus库
import 'package:permission_handler/permission_handler.dart'; // 导入permission_handler库
import 'package:flutter/material.dart'; // 导入material库
import 'package:http/http.dart' as http; // 导入http库
import 'package:workmanager/workmanager.dart';
import 'login_ecjtu_wifi.dart';
import 'notice.dart'; // 通知库
import 'package:flutter_secure_storage/flutter_secure_storage.dart'; // 安全储存数据

// 创建存储
const storage = FlutterSecureStorage();

// 是否第一次运行
Future<void> firstRun() async {
  String? value = await storage.read(key: 'verifyAccount');
  if (value == null) {
    await initializeData();
    return;
  } else if (value == "1") {
    final info = NetworkInfo();
    String? wifiName = await info.getWifiName();
    if (wifiName == '"ECJTU-Stu"' || wifiName == '"EcjtuLib_Free"') {
      try {
        // 检查是否同时连接了校园网和移动数据
        await http
            .get(Uri.parse(drUrl))
            .timeout(const Duration(milliseconds: 500));
        try {
          await http
              .get(Uri.parse(baiduUrl))
              .timeout(const Duration(milliseconds: 1000));
          return;
        } catch (e) {
          await linkWifi(wifiName); // 登入
          try {
            await http
                .get(Uri.parse(baiduUrl))
                .timeout(const Duration(milliseconds: 500));
            // 显示已经登入校园网的消息
            notificationHelper.showNotification(
              title: '自动登入',
              body: '已帮你自动登入校园网，请手动退出程序',
            );
            return;
          } catch (e) {
            notificationHelper.showNotification(
              title: '失败',
              body: '请检查学号，密码，运营商是否正确',
            );
            return;
          }
        }
      } catch (e) {
        notificationHelper.showNotification(
          title: '错误',
          body: '在连接校园网时，请先关闭移动数据后，再运行',
        );
        return;
      }
    }
  }
}

// 后台运行监控校园网
Future<void> backgroundRun() async {
  String? value = await storage.read(key: 'verifyAccount');
  if (value == "1") {
    final info = NetworkInfo();
    String? wifiName = await info.getWifiName();
    if (wifiName == '"ECJTU-Stu"' || wifiName == '"EcjtuLib_Free"') {
      try {
        // 检查是否同时连接了校园网和移动数据
        await http
            .get(Uri.parse(drUrl))
            .timeout(const Duration(milliseconds: 500));
        try {
          await http
              .get(Uri.parse(baiduUrl))
              .timeout(const Duration(milliseconds: 1000));
          return;
        } catch (e) {
          await linkWifi(wifiName); // 登入
          try {
            await http
                .get(Uri.parse(baiduUrl))
                .timeout(const Duration(milliseconds: 500));
            // 显示已经登入校园网的消息
            notificationHelper.showNotification(
              title: '自动登入',
              body: '已帮你自动登入校园网，持续监测中……',
            );
            return;
          } catch (e) {
            notificationHelper.showNotification(
              title: '登入失败',
              body: '请检查学号，密码，运营商是否正确',
            );
            return;
          }
        }
      } catch (e) {
        notificationHelper.showNotification(
          title: '错误',
          body: '在连接校园网时，请先关闭移动数据后，再运行',
        );
        return;
      }
    } else {
      notificationHelper.showNotification(
        title: '检测到未连接校园网',
        body: '后台监测功能已退出',
      );
      Workmanager().cancelAll(); // 取消后台任务
      return;
    }
  }
}

// 已通过验证
Future<void> verifyAccount() async {
  await storage.write(key: 'verifyAccount', value: '1');
}

// 保存账户数据
Future<void> saveData(String username, String password, String operator) async {
  await storage.write(key: 'username', value: username);
  await storage.write(key: 'password', value: password);
  await storage.write(key: 'operator', value: operator);
  await storage.write(key: 'operatorLast', value: changeOperatorLast(operator));
}

// 初始化数据，或删除数据
Future<void> initializeData() async {
  await storage.write(key: 'username', value: "");
  await storage.write(key: 'password', value: "");
  await storage.write(key: 'operator', value: "");
  await storage.write(key: 'operatorLast', value: "");
}

String changeOperatorLast(String operator) {
  if (operator == "中国移动") {
    return "@cmcc";
  } else if (operator == "中国电信") {
    return "@telecom";
  } else if (operator == "中国联通") {
    return "@unicom";
  } else {
    return "-1";
  }
}

Future<Map<String, String>> getPostData() async {
  String username = await storage.read(key: 'username') ?? '';
  String password = await storage.read(key: 'password') ?? '';
  String operatorLast = await storage.read(key: 'operatorLast') ?? '';
  return {
    "DDDDD": ",0,$username$operatorLast",
    "upass": password,
    "R1": "0",
    "R2": "0",
    "R3": "0",
    "R6": "0",
    "para": "00",
    "0MKKey": "123456",
    "buttonClicked": "",
    "redirect_url": "",
    "err_flag": "",
    "username": "",
    "password": "",
    "user": "",
    "cmd": "",
    "Login": "",
  };
}

Future<Map<String, String>> getPostFreeData() async {
  String username = await storage.read(key: 'username') ?? '';
  String password = await storage.read(key: 'password') ?? '';
  return {
    "DDDDD": ",0,$username",
    "upass": password,
    "R1": "0",
    "R2": "0",
    "R3": "0",
    "R6": "0",
    "para": "00",
    "0MKKey": "123456",
    "buttonClicked": "",
    "redirect_url": "",
    "err_flag": "",
    "username": "",
    "password": "",
    "user": "",
    "cmd": "",
    "Login": "",
  };
}

// 显示消息
void showMessage(BuildContext context, String message, {String title = "提示"}) {
  try {
    // 获取可以用于 showDialog 的 NavigatorState
    NavigatorState? navigatorState = Navigator.of(context, rootNavigator: true);
    showDialog(
      context: navigatorState.context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(title),
          content: Text(message),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('确定'),
            ),
          ],
        );
      },
    );
  } catch (e) {
    notificationHelper.showNotification(
      title: '消息未能正常显示，内容如下：',
      body: message,
    );
  }
}

// 获取位置信息以获取wifi名称
Future<void> requestLocationPermission(BuildContext context) async {
  PermissionStatus status = await Permission.location.status;
  if (!status.isGranted) {
    PermissionStatus newStatus = await Permission.location.request();
    if (!newStatus.isGranted) {
      var text = "为了识别你当前连接的wifi名，\n请允许获取位置信息，\n否则自动登入校园网功能将无法使用。";
      showMessage(context, text);
    } else {
      showMessage(context, "已能识别你当前连接的wifi，请重新运行");
    }
  }
}

// 获取wifi名称
Future<String?> getWifiName(BuildContext context) async {
  await requestLocationPermission(context);
  final info = NetworkInfo();
  String? wifiName = await info.getWifiName();
  return wifiName;
}

// 显示底部消息
DateTime? lastPressTime;
void showBottomMessage(BuildContext context, String message) {
  final now = DateTime.now();
  if (lastPressTime != null && now.difference(lastPressTime!).inSeconds < 1) {
    return;
  }
  lastPressTime = now;

  final snackBar = SnackBar(
    content: Text(message),
    duration: const Duration(seconds: 3), // 信息将在3秒后自动隐藏
  );

  // 显示SnackBar
  ScaffoldMessenger.of(context).showSnackBar(snackBar);
}
