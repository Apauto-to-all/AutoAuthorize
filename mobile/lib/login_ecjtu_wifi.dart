import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'save_and_get.dart';
import 'notice.dart';

const baiduUrl = 'https://www.baidu.com/';
const drUrl = 'http://172.16.2.100/';

Future<String> getLoginUrl() async {
  final response = await http.get(Uri.parse(drUrl));
  final html = response.body;

  final ip4YMatch = RegExp("v4ip='(.*?)';", dotAll: true).firstMatch(html);

  String ip4;
  if (ip4YMatch == null) {
    final ip4NMatch = RegExp("v46ip='(.*?)' ", dotAll: true).firstMatch(html);
    ip4 = ip4NMatch!.group(1)!;
  } else {
    ip4 = ip4YMatch.group(1)!;
  }

  return 'http://172.16.2.100:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.16.2.100&iTermType=1'
      '&wlanuserip=$ip4&wlanacip=null&wlanacname=null&mac=00-00-00-00-00-00&ip=$ip4&enAdvert=0'
      '&queryACIP=0&loginMethod=1';
}

Future<void> logout() async {
  final response = await http.get(Uri.parse(drUrl));
  final html = response.body;

  final macMatch = RegExp("olmac='(.*?)'", dotAll: true).firstMatch(html);
  String? mac;
  if (macMatch != null && macMatch.group(1) != null) {
    mac = macMatch.group(1);

    final urlOut =
        'http://172.16.2.100:801/eportal/?c=ACSetting&a=Logout&wlanuserip=null&wlanacip=null&wlanacname=null'
        '&port=&hostname=172.16.2.100&iTermType=1&session=null&queryACIP=0&mac=$mac';

    final postDataOut = {
      'c': 'ACSetting',
      'a': 'Logout',
      'wlanuserip': 'null',
      'wlanacname': 'null',
      'port': '',
      'hostname': '172.16.2.100',
      'iTermType': '1',
      'session': 'null',
      'queryACIP': '0',
      'mac': mac,
    };
    await http.post(Uri.parse(urlOut), body: postDataOut);
  }
}

Future<int> verifyWifi(BuildContext context) async {
  String? wifiName = await getWifiName(context);
  if (wifiName == '"ECJTU-Stu"' || wifiName == '"EcjtuLib_Free"') {
    try {
      await http
          .get(Uri.parse(baiduUrl))
          .timeout(const Duration(milliseconds: 500));
      return 4; // 连接了校园网，已登入
    } catch (e) {
      return 3; // 连接了校园网，但未登入
    }
  } else {
    try {
      await http
          .get(Uri.parse(baiduUrl))
          .timeout(const Duration(milliseconds: 500));
      return 2; // 已连接其他网络
    } catch (e) {
      return 1; // 网络未连接
    }
  }
}

Future<void> saveAndVerify(BuildContext context, String username,
    String password, String? operator) async {
  var wifiName = await getWifiName(context);
  if (wifiName == '"ECJTU-Stu"' || wifiName == '"EcjtuLib_Free"') {
    if (username.isEmpty || password.isEmpty || operator == null) {
      showMessage(context, '账号，密码，运营商（如果你不使用ECJTU-Stu请随意填）不能为空');
      return;
    } else {
      await saveData(username, password, operator);
      // 管他三七二十一，先登出校园网
      await logout();
      // 连接了校园网，但未登入
      await linkWifi(wifiName); // 登入
      try {
        await http
            .get(Uri.parse(baiduUrl))
            .timeout(const Duration(milliseconds: 500));
        showMessage(context, '验证成功，你的账号已经保存');
        await verifyAccount();
        showBottomMessage(context, '你已经登入校园网');
        return;
      } catch (e) {
        showMessage(context, '验证失败，请检查账号密码或运营商是否正确');
        return;
      }
    }
  } else {
    showMessage(context, '请连接校园网');
  }
}

// 连接校园网
Future<void> linkWifi(String? wifiName) async {
  if (wifiName == '"ECJTU-Stu"') {
    await linkText(); // 登入校园网，测试
    // Map<String, String> postData = await getPostData();
    // await http.post(Uri.parse(getLoginUrl() as String), body: postData);
  } else if (wifiName == '"EcjtuLib_Free"') {
    Map<String, String> postFreeData = await getPostFreeData();
    await http.post(Uri.parse(getLoginUrl() as String), body: postFreeData);
  }
}

// 立即连接校园网
Future<void> linkWifiNow(BuildContext context) async {
  String? value = await storage.read(key: 'verifyAccount');
  if (value == '1') {
    String? wifiName = await getWifiName(context);
    if (wifiName == '"ECJTU-Stu"' || wifiName == '"EcjtuLib_Free"') {
      try {
        await http
            .get(Uri.parse(baiduUrl))
            .timeout(const Duration(milliseconds: 500));
        showBottomMessage(context, '你已经登入校园网');
      } catch (e) {
        await linkWifi(wifiName); // 登入
        try {
          await http
              .get(Uri.parse(baiduUrl))
              .timeout(const Duration(milliseconds: 500));
          showBottomMessage(context, '成功，已经登入校园网');
        } catch (e) {
          showBottomMessage(context, '失败，请检查账号密码或运营商是否正确');
        }
      }
    } else {
      showMessage(context, '请连接校园网');
    }
  } else {
    showMessage(context, '请先保存账户并验证');
  }
}

// 登入校园网测试
Future<void> linkText() async {
  Map<String, String> postFreeData = await getPostFreeData();
  String loginUrl = await getLoginUrl();
  await http.post(Uri.parse(loginUrl), body: postFreeData);
}

Future<void> text(BuildContext context) async {
  notificationHelper.showNotification(
    title: 'Hello',
    body: 'This is a notification!',
  );
}
