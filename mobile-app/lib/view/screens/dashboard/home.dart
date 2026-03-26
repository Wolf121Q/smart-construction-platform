import 'package:awesome_dialog/awesome_dialog.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_preferences_session.dart';
import 'package:dha_ctt_app/view/screens/dashboard/dashboard.dart';
import 'package:dha_ctt_app/view/screens/dashboard/drawer/custom_drawer.dart';
import 'package:dha_ctt_app/view/screens/login/login.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:shrink_sidemenu/shrink_sidemenu.dart';

class Home extends StatefulWidget {
  final String? arguments2;
  final String? arguments1;
  const Home({super.key, this.arguments2, this.arguments1});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> with TickerProviderStateMixin {
  final GlobalKey<SideMenuState> _endSideMenuKey = GlobalKey<SideMenuState>();
  bool isOpened = false;
  String? apiChacker;
  // final _drawerController = ZoomDrawerController();

  toggleMenu([bool end = false]) {
    if (end) {
      final _state = _endSideMenuKey.currentState!;
      if (_state.isOpened) {
        _state.closeSideMenu();
        apiChacker = 'Default1';
      } else {
        _state.openSideMenu();
        apiChacker = 'Default1';
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    // Retrieve the argument value

    print('api chker value $apiChacker');

    if (apiChacker == 'login') {
      // Store default value
      // You can replace the code below with your actual logic for storing the default value
      apiChacker = 'Default';
    }
    if (apiChacker == 'Default1') {
      apiChacker == 'Default';
    } else {
      // Do something else if apiChacker is not equal to 'login'
      // Replace the code below with your actual logic
      apiChacker = Get.arguments ?? 'Default';
    }
    print('api chker value 1 $apiChacker');
    return SideMenu(
      key: _endSideMenuKey,
      inverse: false, // end side menu

      background: appcolor,
      // radius: BorderRadius.circular(50),

      type: SideMenuType.shrinkNSlide,

      closeIcon: Icon(
        color: dfColor,
        Icons.close,
        size: 30,
      ),

      menu: Padding(
        padding: const EdgeInsets.only(left: marginLR + 10, right: 0),
        child: CustomDrawer(),
      ),
      onChange: (_isOpened) {
        setState(() => isOpened = isOpened);
      },
      child: Scaffold(
          backgroundColor: greyColor,
          appBar: AppBar(
            elevation: 0,
            actions: [
              Container(
                width: scWidth / 11,
                margin: EdgeInsets.only(left: marginLR),
                alignment: Alignment.center,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: dfColor,
                    padding: EdgeInsets.all(0),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  onPressed: () => toggleMenu(true),
                  child: Image.asset(
                    "asserts/icons/leftmenu.png",
                    width: scWidth / 16,
                    color: appcolor,
                  ),
                ),
              ),
              Container(
                // alignment: Alignment.center,
                margin: EdgeInsets.only(top: 15, left: scWidth / 6),
                child: Text(
                  "Company City",
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: dfColor,
                    fontWeight: FontWeight.w700,
                    fontSize: lgFontSize,
                  ),
                ),
              ),
              Spacer(),
              Container(
                width: scWidth / 11,
                margin: EdgeInsets.only(right: 5),
                alignment: Alignment.center,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: dfColor,
                    padding: EdgeInsets.all(0),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  onPressed: () {
                    CustomDialog(context);
                  },
                  child: Icon(
                    Icons.info_outline,
                    color: appcolor,
                    size: scWidth / 16,
                  ),
                ),
              ),
              Container(
                width: scWidth / 11,
                margin: EdgeInsets.only(right: marginLR),
                alignment: Alignment.center,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: dfColor,
                    padding: EdgeInsets.all(0),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  onPressed: () {
                    AwesomeDialog(
                      context: context,
                      dialogType: DialogType.noHeader,
                      animType: AnimType.bottomSlide,
                      title: 'Logout',
                      desc: 'Are you sure you want to logout?',
                      btnCancel: IconButton(
                        onPressed: () {
                          Navigator.pop(context); // Close the dialog
                        },
                        icon: Image.asset(
                          'asserts/icons/cross.png',
                          width: 40,
                        ),
                        color: Colors.red,
                      ),
                      btnOk: IconButton(
                        onPressed: () async {
                          //  await

                          logout();
                          final box = GetStorage();
                          box.remove(LocalDBStrings.login_user);
                          Get.offAll(() => LogIn());
                        },
                        icon: Image.asset(
                          'asserts/icons/checked.png',
                          width: 40,
                        ),
                        color: Colors.green,
                      ),
                    ).show();
                  },
                  child: Icon(
                    Icons.logout,
                    size: scWidth / 16,
                    color: appcolor,
                  ),
                ),
              ),
            ],
            backgroundColor: appcolor,
          ),
          body: Dashboard(apiChacker, widget.arguments2)),
    );
  }
}
