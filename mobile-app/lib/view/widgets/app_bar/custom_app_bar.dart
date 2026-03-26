import 'package:dha_ctt_app/constant.dart';

import 'package:flutter/material.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final navFunction;
  final infoFunction;
  final IconData lastIcon;

  CustomAppBar(
      {required this.navFunction,
      required this.lastIcon,
      required this.infoFunction});
  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return AppBar(
      // elevation: 0,
      centerTitle: true,
      backgroundColor: appcolor,
      title: Text(
        'Company City',
        style: TextStyle(
          color: dfColor,
          fontWeight: FontWeight.w700,
          fontSize: lgFontSize,
        ),
      ),
      leading: Container(
        width: scWidth / 11,
        // height: scheight / 12,
        margin: EdgeInsets.only(left: marginLR),
        alignment: Alignment.center,
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: dfColor,
            padding: EdgeInsets.all(0),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
          ),
          onPressed: () => navFunction()

          // Navigator.pushAndRemoveUntil(
          //   context,
          //   MaterialPageRoute(builder: (context) => const Home()),
          //   (Route<dynamic> route) =>
          //       false, // This ensures all previous routes are removed
          // );

          // Navigator.of(context).pop();

          ,
          child: Icon(
            Icons.arrow_back,
            size: scWidth / 16,
            color: appcolor,
          ),
        ),
      ),
      actions: [
        Container(
          width: scWidth / 11,
          margin: EdgeInsets.only(right: marginLR),
          alignment: Alignment.center,
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: dfColor,
              padding: EdgeInsets.all(0),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15),
              ),
            ),
            onPressed: () {
              infoFunction();
            },
            child: Icon(
              lastIcon,
              size: scWidth / 16,
              color: appcolor,
            ),
          ),
        ),
      ],
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}
