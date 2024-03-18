import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'save_and_get.dart';

const baiduUrl = 'https://www.baidu.com/';
const drUrl = 'http://172.16.2.100/';

Future<String> getLoginUrl() async {
  try {
    final response = await http.get(Uri.parse(drUrl));
    final html = response.body;

    final ip4NMatch = RegExp("v46ip='(.*?)' ", dotAll: true).firstMatch(html);

    String ip4;
    if (ip4NMatch != null) {
      ip4 = ip4NMatch.group(1)!;
    } else {
      final ip4YMatch = RegExp("v4ip='(.*?)';", dotAll: true).firstMatch(html);
      if (ip4YMatch != null) {
        ip4 = ip4YMatch.group(1)!;
      } else {
        ip4 = '';
      }
    }
    return 'http://172.16.2.100:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.16.2.100&iTermType=1'
        '&wlanuserip=$ip4&wlanacip=null&wlanacname=null&mac=00-00-00-00-00-00&ip=$ip4&enAdvert=0'
        '&queryACIP=0&loginMethod=1';
  } catch (e) {
    return '';
  }
}

Future<void> logout(final response) async {
  try {
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
  } catch (e) {
    return;
  }
}

Future<void> saveAndVerify(BuildContext context, String username,
    String password, String? operator) async {
  var wifiName = await getWifiName(context);
  if (wifiName == '"ECJTU-Stu"' || wifiName == '"EcjtuLib_Free"') {
    if (username.isEmpty || password.isEmpty || operator == null) {
      showMessage(context, '学号，密码，运营商（如果不使用ECJTU-Stu请随意填）不能为空');
      return;
    } else {
      showBottomMessage(context, '正在验证，请稍安勿躁……勿重复点击');
      // 检查是否同时连接了校园网和移动数据
      try {
        final response = await http
            .get(Uri.parse(drUrl))
            .timeout(const Duration(milliseconds: 500));
        // 先保存账户数据，等下测试登入时要用到
        await saveData(username, password, operator);
        // 管他三七二十一，先登出校园网
        await logout(response);
        // 连接了校园网，但未登入
        await linkWifi(wifiName); // 登入
        try {
          await http
              .get(Uri.parse(baiduUrl))
              .timeout(const Duration(milliseconds: 500));
          showMessage(context, '验证成功，你的信息已经保存');
          await verifyAccount(); // 已通过验证
          showBottomMessage(context, '你已经登入校园网');
          return;
        } catch (e) {
          showMessage(context, '验证失败，请检查学号，密码或运营商是否正确');
          return;
        }
      } catch (e) {
        showMessage(context, '你连接了校园网WiFi，同时打开了移动数据，程序无法工作，请关闭移动数据后再试');
        return;
      }
    }
  } else {
    showMessage(context, '请连接校园网');
    return;
  }
}

// 连接校园网，主功能
Future<void> linkWifi(String? wifiName) async {
  if (wifiName == '"ECJTU-Stu"') {
    await linkText(); // 需要删除，仅用于测试
    // Map<String, String> postData = await getPostData();
    // String loginUrl = await getLoginUrl();
    // await http.post(Uri.parse(loginUrl), body: postData);
  } else if (wifiName == '"EcjtuLib_Free"') {
    Map<String, String> postFreeData = await getPostFreeData();
    String loginUrl = await getLoginUrl();
    await http.post(Uri.parse(loginUrl), body: postFreeData);
  }
}

// 立即连接校园网
Future<void> linkWifiNow(BuildContext context) async {
  String? value = await storage.read(key: 'verifyAccount');
  if (value == '1') {
    String? wifiName = await getWifiName(context);
    if (wifiName == '"ECJTU-Stu"' || wifiName == '"EcjtuLib_Free"') {
      // 检查是否同时连接了校园网和移动数据
      try {
        await http
            .get(Uri.parse(drUrl))
            .timeout(const Duration(milliseconds: 500));
        try {
          await http
              .get(Uri.parse(baiduUrl))
              .timeout(const Duration(milliseconds: 500));
          showBottomMessage(context, '你已经登入校园网');
          return;
        } catch (e) {
          await linkWifi(wifiName); // 登入
          try {
            await http
                .get(Uri.parse(baiduUrl))
                .timeout(const Duration(milliseconds: 500));
            showBottomMessage(context, '成功，已经登入校园网');
            return;
          } catch (e) {
            showBottomMessage(context, '失败，请检查学号，密码或运营商是否正确');
            return;
          }
        }
      } catch (e) {
        showBottomMessage(context, '你连接了校园网WiFi，同时打开了移动数据，程序无法工作，请关闭移动数据后再试');
      }
    } else {
      showBottomMessage(context, '请连接校园网');
    }
  } else {
    showBottomMessage(context, '请先保存账户并验证');
  }
}

// 登入校园网测试
Future<void> linkText() async {
  Map<String, String> postFreeData = await getPostFreeData();
  String loginUrl = await getLoginUrl();
  await http.post(Uri.parse(loginUrl), body: postFreeData);
  return;
}
