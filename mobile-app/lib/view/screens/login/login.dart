
import 'package:dha_ctt_app/model/controller/auth_controller.dart';
import 'package:dha_ctt_app/model/resources/values_manager.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_snackbar.dart';
import 'package:flutter/foundation.dart';
import 'package:get/get.dart';
import 'package:overlay_loader_with_app_icon/overlay_loader_with_app_icon.dart';
import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';
import 'dart:io' show Platform;
import '../../../constant.dart';

final getx = GetConnect();

class LogIn extends StatefulWidget {
  static const routeName = '/login';
  @override
  State<LogIn> createState() => _LogInState();
}

class _LogInState extends State<LogIn> {
  bool _isLoading = false;
  final _formKey = GlobalKey<FormState>();
  String _email = '';
  String _password = '';
  bool _showPassword = false;

  void _login(AuthController authController, _email, _password) async {
    if (_email.isEmpty) {
      showCustomSnackBar('enter email address'.tr);
      _isLoading = false;
    } else if (!GetUtils.isEmail(_email)) {
      showCustomSnackBar('enter a valid email address'.tr);
      _isLoading = false;
    } else if (_password.isEmpty) {
      showCustomSnackBar('enter password'.tr);
      _isLoading = false;
    }
    // else if (_password.length < 9) {
    //   showCustomSnackBar('password_should_be '.tr);
    // }

    else {
      authController.login(_email, _password).then((status) async {
        if (status.isSuccess) {
          debugPrint(
              "=======status${status.isSuccess}:${status.message}=======");
          _isLoading = false;
          Get.offAll(
            () => Home(),
            arguments: 'login',
          );
        } else {
          debugPrint(
              "=======status${status.isSuccess}:${status.message}=======");
          showCustomSnackBar(status.message);
          _isLoading = false;
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;

    return GetBuilder<AuthController>(
        init: AuthController(),
        builder: (_) {
          return SafeArea(
            child: Scaffold(
              backgroundColor: lightGrey1,
              body: OverlayLoaderWithAppIcon(
                overlayBackgroundColor: appcolor,
                isLoading: _isLoading,
                appIcon: CircularProgressIndicator(),
                child: SingleChildScrollView(
                  child: Container(
                    alignment: Alignment.center,
                    padding:
                        EdgeInsets.symmetric(horizontal: marginLR + marginLR),
                    color: lightGrey1,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      // crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        // Section 1: Non-scrollable content
                        Container(
                          margin: EdgeInsets.only(top: scHeight / 20),
                          child: Stack(
                            alignment: Alignment.topCenter,
                            children: [
                              Stack(
                                alignment: Alignment.center,
                                children: [
                                  Image.asset(
                                    'asserts/icons/app_icon.png', // Replace with your actual asset path
                                    width: 140,
                                    height: 140,
                                  ),
                                  Shimmer.fromColors(
                                    period: Duration(milliseconds: 2000),
                                    baseColor: Colors.transparent,
                                    highlightColor: Colors.white70,
                                    child: Container(
                                      alignment: Alignment.center,
                                      width: 120,
                                      height: 120,
                                      decoration: BoxDecoration(
                                        borderRadius: BorderRadius.circular(
                                            75), // Adjust as needed
                                        color: Colors.white, // Adjust as needed
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              Container(
                                margin: Platform.isAndroid
                                    ? EdgeInsets.only(top: scHeight / 5.1)
                                    : EdgeInsets.only(top: scHeight / 5.7),
                                child: Column(
                                  children: [
                                    Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: [
                                        Text(
                                          "Located ",
                                          style: TextStyle(
                                              color: appcolorlabel,
                                              fontSize: 20,
                                              fontWeight: FontWeight.bold),
                                        ),
                                        Text(
                                          "City",
                                          style: TextStyle(
                                              color: appcolorlabel,
                                              fontSize: 18,
                                              fontWeight: FontWeight.bold),
                                        ),
                                      ],
                                    ),
                                    Container(
                                      margin: EdgeInsets.only(
                                          bottom: marginLR + 30),
                                      child: Text(
                                        "Your Company Name",
                                        style: TextStyle(
                                          color: appcolorlabel,
                                          fontSize: 18,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),

                        // Section 2: Scrollable content
                        Container(
                          child: Form(
                            key: _formKey,
                            child: Container(
                              margin: EdgeInsets.only(bottom: 0),
                              child: Column(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Container(
                                    margin: EdgeInsets.only(top: AppSize.s30),
                                    child: TextFormField(
                                      autofocus: false,
                                      decoration: InputDecoration(
                                        prefixIconColor: blackColor,
                                        suffixIconColor: blackColor,
                                        labelStyle:
                                            TextStyle(color: blackColor),
                                        labelText: 'Username or Email',
                                        prefixIcon: Icon(
                                          Icons.email_outlined,
                                          size: dfIconSize,
                                        ),
                                        border: OutlineInputBorder(
                                          borderRadius: BorderRadius.circular(
                                              roundloginField),
                                        ),
                                        filled: true,
                                        fillColor: dfColor,
                                        contentPadding: const EdgeInsets.only(
                                            left: 35.0,
                                            bottom: marginLR + 5,
                                            top: marginLR + 5),
                                        focusedBorder: OutlineInputBorder(
                                          borderSide:
                                              BorderSide(color: blackColor),
                                          borderRadius: BorderRadius.circular(
                                              roundloginField),
                                        ),
                                      ),
                                      style: TextStyle(
                                          fontSize: dfFontSize,
                                          color: blackColor),
                                      keyboardType: TextInputType.emailAddress,
                                      // validator: validateEmail,
                                      onChanged: (value) {
                                        setState(() {
                                          _email = value.trim();
                                        });
                                      },
                                    ),
                                  ),
                                  //////////////////
                                  Container(
                                    margin: EdgeInsets.symmetric(vertical: 20),
                                    child: Column(
                                      // crossAxisAlignment:
                                      //     CrossAxisAlignment.stretch,
                                      // mainAxisAlignment:
                                      //     MainAxisAlignment.spaceBetween,
                                      children: [
                                        Container(
                                          margin: EdgeInsets.only(top: 8),
                                          child: TextFormField(
                                            autofocus: false,
                                            style: TextStyle(
                                                fontSize: dfFontSize,
                                                color: blackColor),
                                            decoration: InputDecoration(
                                              prefixIconColor: blackColor,
                                              suffixIconColor: blackColor,
                                              labelStyle:
                                                  TextStyle(color: blackColor),
                                              labelText: 'Password',
                                              prefixIcon: Icon(
                                                Icons.lock_outlined,
                                                size: dfIconSize,
                                              ),
                                              border: OutlineInputBorder(
                                                borderRadius:
                                                    BorderRadius.circular(
                                                        roundloginField),
                                              ),
                                              filled: true,
                                              fillColor: dfColor,
                                              contentPadding:
                                                  const EdgeInsets.only(
                                                      left: 35.0,
                                                      bottom: marginLR + 5,
                                                      top: marginLR + 5),
                                              focusedBorder: OutlineInputBorder(
                                                borderSide: BorderSide(
                                                    color: blackColor),
                                                borderRadius:
                                                    BorderRadius.circular(
                                                        roundloginField),
                                              ),
                                              suffixIcon: IconButton(
                                                icon: Icon(
                                                  _showPassword
                                                      ? Icons.visibility
                                                      : Icons.visibility_off,
                                                ),
                                                onPressed: () {
                                                  setState(() {
                                                    _showPassword =
                                                        !_showPassword;
                                                  });
                                                },
                                              ),
                                            ),
                                            obscureText:
                                                !_showPassword, // Toggle visibility
                                            //  validator: validatePassword,
                                            onChanged: (value) {
                                              setState(() {
                                                _password = value.trim();
                                              });
                                            },
                                          ),
                                        ),
                                        Container(
                                          margin: EdgeInsets.symmetric(
                                              horizontal: 5, vertical: 10),
                                          child: Column(children: [
                                            Container(
                                              margin: EdgeInsets.symmetric(
                                                  vertical: 10),
                                              child: Row(
                                                mainAxisAlignment:
                                                    MainAxisAlignment.end,
                                                children: [
                                                  // Text(
                                                  //   "Forgot Password?",
                                                  //   style: TextStyle(
                                                  //       color: lightappcolor,
                                                  //       fontWeight:
                                                  //           FontWeight.w700),
                                                  // ),
                                                ],
                                              ),
                                            ),
                                          ]),
                                        ),
                                        Container(
                                          margin: EdgeInsets.only(
                                            top: 0,
                                          ),
                                          width: scWidth,
                                          child: ElevatedButton(
                                            onPressed: () {
                                              if (_formKey.currentState!
                                                  .validate()) {
                                                print(
                                                    'Email: $_email, Password: $_password');
                                                _isLoading = true;
                                                if (defaultTargetPlatform ==
                                                    TargetPlatform.android) {
                                                  _login(_, _email, _password);
                                                } else if (defaultTargetPlatform ==
                                                    TargetPlatform.iOS) {
                                                  _login(_, _email, _password);
                                                }
                                              }
                                            },
                                            child: Text(
                                              'LOGIN',
                                              style: TextStyle(
                                                  color: btnTextColor,
                                                  fontWeight: FontWeight.bold),
                                            ),
                                            style: ElevatedButton.styleFrom(
                                              backgroundColor: appcolor,
                                              padding: EdgeInsets.symmetric(
                                                  vertical: 15),
                                              shape: RoundedRectangleBorder(
                                                borderRadius:
                                                    BorderRadius.circular(30),
                                              ),
                                            ),
                                          ),
                                        ),
                                        Container(
                                          margin: EdgeInsets.only(
                                            top: scHeight / 18,
                                          ),
                                          width: scWidth,
                                          child: Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.center,
                                            children: [
                                              Text(
                                                'For Any Query Please Call At: ',
                                                style: TextStyle(
                                                    color: Colors.black87,
                                                    fontSize: dfFontSize),
                                              ),
                                              Text(
                                                '2525',
                                                style: TextStyle(
                                                    color: Colors.black87,
                                                    fontWeight: FontWeight.w600,
                                                    fontSize: dfFontSize),
                                              ),
                                              GestureDetector(
                                                onTap: () {
                                                  // Handle the tap event
                                                  CustomDialog(context);
                                                },
                                                child: Container(
                                                  margin: EdgeInsets.only(
                                                      left: marginLR - 5),
                                                  child: Icon(
                                                    Icons.info_outline,
                                                    size: dfIconSize + 10,
                                                    color: Colors.black54,
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                        GestureDetector(
                                          onTap: () {
                                            // Handle the tap event
                                            CustomDialog(context);
                                          },
                                          child: Container(
                                            padding: EdgeInsets.symmetric(
                                                vertical: 5),
                                            margin: EdgeInsets.only(
                                              top: 65,
                                            ),
                                            width: scWidth,
                                            decoration: BoxDecoration(
                                              borderRadius:
                                                  BorderRadius.circular(5),
                                              color: appcolorlabel,
                                            ),
                                            child: Row(
                                              mainAxisAlignment:
                                                  MainAxisAlignment.spaceAround,
                                              children: [
                                                Text(
                                                  'Powered By ',
                                                  style: TextStyle(
                                                      color: Colors.white,
                                                      fontSize: dfFontSize,
                                                      fontWeight:
                                                          FontWeight.w900),
                                                ),
                                                Row(
                                                  children: [
                                                    Text(
                                                      'Claystone',
                                                      style: TextStyle(
                                                        color: applightcolor,
                                                        fontWeight:
                                                            FontWeight.w600,
                                                        fontSize: dfFontSize,
                                                      ),
                                                    ),
                                                    Text(
                                                      ' Tech',
                                                      style: TextStyle(
                                                          color: appcolor,
                                                          fontWeight:
                                                              FontWeight.w600,
                                                          fontSize: dfFontSize),
                                                    ),
                                                  ],
                                                ),
                                              ],
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          );
        });
  }
}
