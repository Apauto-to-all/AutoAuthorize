import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter/services.dart';
import 'save_and_get.dart';
import 'ui.dart';

// 重要的事情说三遍
const importantText = '''
！！！一定要允许位置信息请求！！！
！！！一定要允许位置信息请求！！！
！！！一定要允许位置信息请求！！！
重要的事情说三遍
若不同意，很抱歉，无法为你提供服务
（具体原因，请往下看……）''';

const readMe = '''
1.关闭移动数据（如果不关闭移动数据，程序“很有可能”无法帮你登入校园网）

2.连接校园网（不连校园网，怎么使用？）

2.输入学号，密码，选择运营商（如果你不使用ECJTU-Stu请随意输入，确认无误无误后进行下一步）

3.点击“保存账户并验证”按钮（第一次使用，需要你允许获取位置信息请求，为什么？我们可以通过你的位置信息，获取你当前连接的WiFi名字，用来判断你是否连接校园网，连接ECJTU-Stu还是EcjtuLib_Free。别担心，我们不会用于其他目的，代码已开源，不放心可以自行编译）


4.点击后请等候一段时间（程序会尝试用你提供的账户信息，帮你登入校园网，如果你已经是登入状态，也无需担心，程序会自动帮你退出校园网，然后再运行自动登入功能，如果登入成功，说明你提供的信息是正确的，我们会保存你的账户信息，并通过验证，接下来，就可以愉快使用我们的功能啦）

5.通过验证后，解锁以下功能：
（1）可以点击右下角的按钮，帮你登入校园网。
（2）如果本程序运行在后台，在需要登入校园网时，直接切换过来，就能自动为你登入校园网。（参考了另一位同学开发的登入校园网程序）
（3）如果你连接了校园网，并重新打开我们的程序，在未登入情况下，程序会自动帮你登入校园网，然后自动退出程序，并利用通知告诉你登入情况。（全自动！不过还是需要你在连接校园网后，再运行本程序，目前没实现：检测到你连接校园网wifi，就帮你自动帮你登入。我感觉……用处不大，之后就看你们的反馈吧，毕竟电脑版的已经实现了后台监测功能）

6.注意：
（1）如果你需要更换学号，密码或运营商，请点击“修改账户”按钮，否则，我们会一直使用你之前通过验证时保存的账户信息。
（2）不同用户的不同网络情况，我们还没能完全覆盖到，可能会出现一些错误提示信息，如果你遇到了，请重新尝试，如果影响比较严重，可以联系我。
（3）如果你需要使用校园网，请务必先关闭移动数据，然后打开WiFi，选择校园网进行连接，最后打开本程序进行自动登入，如果你没关闭移动数据，程序“很有可能”无法帮你登入校园网。
（4）不要通知本程序的通知权限，本程序的通知只显示6秒，到期自动清除通知，不会打扰到你，但是会帮你及时了解到程序的运行情况。（除了第5条的功能3，程序帮你登入校园网后，直接退出，来不及帮你自动清除通知，需要你手动在状态栏清除通知）

''';

const myWords = '''
如果你喜欢该项目，可以给我一颗免费的star，
也可以“请我喝瓶矿泉水”（我也挺喜欢白嫖的，看看就好），
好程序大家用，如果你觉得好用可以帮忙推广一下，谢谢！''';

// 打开URL
void launchURL(String url) async {
  var uri = Uri.parse(url);
  if (await canLaunchUrl(uri)) {
    await launchUrl(uri);
  } else {
    return;
  }
}

void copyText(BuildContext context, String copyText) {
  Clipboard.setData(ClipboardData(text: copyText));
  showMessage(context, '$copyText已复制到剪贴板');
}

void showReadMe(BuildContext context) {
  showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    backgroundColor: textBackgroundColor,
    builder: (context) {
      return const UiReadMe();
    },
  );
}

class UiReadMe extends StatefulWidget {
  const UiReadMe({super.key});

  @override
  UiReadMeState createState() => UiReadMeState();
}

class UiReadMeState extends State<UiReadMe> {
  bool _isExpanded = false; // 是否展开，用于显示具体使用步骤

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.8,
      decoration: const BoxDecoration(
        color: textBackgroundColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      child: ListView(
        children: <Widget>[
          const Text(
            "使用说明",
            style: TextStyle(
              fontSize: 30,
            ),
            textAlign: TextAlign.center, // 让文字居中显示
          ),
          const Divider(
            color: textColor,
            height: 1,
          ),
          const Text(
            importantText,
            style: TextStyle(
              fontSize: 20,
            ),
            textAlign: TextAlign.center, // 让文字居中显示
          ),
          const Divider(
            color: textColor,
            height: 1,
          ),
          ListTile(
            title: const Text(
              '具体使用步骤：',
              style: TextStyle(fontSize: 25),
            ),
            subtitle: const Text(
              '（点击右边图标展开文本）',
              style: TextStyle(fontSize: 18),
            ),
            onTap: () {
              setState(() {
                _isExpanded = !_isExpanded;
              });
            },
            trailing: _isExpanded
                ? const Icon(Icons.menu_book)
                : const Icon(Icons.book),
          ),
          Text(
            readMe,
            style: const TextStyle(
              fontSize: 20,
            ),
            maxLines: _isExpanded ? null : 2,
            overflow:
                _isExpanded ? TextOverflow.visible : TextOverflow.ellipsis,
          ),
          const Divider(
            color: textColor,
            height: 1,
          ),
          ListTile(
            title: const Text(
              '打开github项目地址',
              style: TextStyle(
                fontSize: 20,
                color: Colors.blue,
                decoration: TextDecoration.underline,
              ),
            ),
            onTap: () =>
                launchURL("https://github.com/Apauto-to-all/AutoAuthorize"),
            trailing: const Icon(Icons.launch, color: Colors.blue),
          ),
          ListTile(
            title: const Text(
              '打开蓝奏云网盘地址',
              style: TextStyle(
                fontSize: 20,
                color: Colors.blue,
                decoration: TextDecoration.underline,
              ),
            ),
            subtitle: const Text(
              '提取码：ecjt',
              style: TextStyle(fontSize: 18),
            ),
            onTap: () {
              copyText(context, 'ecjt');
              launchURL("https://www.lanzoub.com/b052h91gb?pass=ecjt");
            },
            trailing: const Icon(Icons.launch, color: Colors.blue),
          ),
          const Divider(
            color: textColor,
            height: 1,
          ),
          const Text(
            myWords,
            textAlign: TextAlign.center, // 让文字居中显示
            style: TextStyle(
              fontSize: 20,
            ),
          ),
          Image.asset(
            "images/ds.png",
            fit: BoxFit.fill,
          ),
          const Text(
            '浩瀚江海，源于点滴的汇聚',
            textAlign: TextAlign.center, // 让文字居中显示
            style: TextStyle(
              fontSize: 20,
            ),
          ),
          const Divider(
            color: textColor,
            height: 1,
          ),
          ListTile(
            title: const Text(
              '联系我',
              style: TextStyle(fontSize: 20),
            ),
            subtitle: const Text(
              '点击复制我的邮箱地址',
              style: TextStyle(fontSize: 18),
            ),
            onTap: () => copyText(context, 'atuzkb@outlook.com'),
            trailing: const Icon(Icons.email),
          ),
        ],
      ),
    );
  }
}
