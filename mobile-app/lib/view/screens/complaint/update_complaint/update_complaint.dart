import 'dart:io';
import 'dart:math';
import 'package:connectivity/connectivity.dart';
import 'package:dha_ctt_app/animation/animated_checkmark_dialog.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/widgets/app_bar/custom_app_bar.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/card_Image_widget.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';
import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/complaint_status_model.dart';
import 'package:dio/dio.dart';

import 'package:dropdown_textfield/dropdown_textfield.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:overlay_loader_with_app_icon/overlay_loader_with_app_icon.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:geolocator/geolocator.dart';

import 'package:image_picker/image_picker.dart';


/// Flutter code sample for DropdownButton.

class UpdateComplaint extends StatefulWidget {
  final String userId;

  const UpdateComplaint({
    required this.userId,
  });

  @override
  State<UpdateComplaint> createState() => _UpdateComplaintState();
}

class _UpdateComplaintState extends State<UpdateComplaint> {
  SingleValueDropDownController? _cnt;
  SingleValueDropDownController? _Subcnt;
  final _formKey = GlobalKey<FormState>();

  dynamic _status;
  dynamic _statusId;

  String _description = '';
  String _progress = '';
  String _source = '';
  dynamic path = '';
  String? latitude;
  String? longitude;
  String? currentTime;

  List<DropDownValueModel> complaintStatus = [];
  List<ComplaintStatusesModel> complaintStatusesModel = [];

  int selectedCategory = 0;
  String filePath = '';
  bool _isLoading = false;

  Future<bool> isInternetConnected() async {
    var connectivityResult = await (Connectivity().checkConnectivity());
    return connectivityResult != ConnectivityResult.none;
  }

  // Function to retrieve status from SharedPreferences and populate the list
  Future<void> getStatusFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? statusDataSerialzed = prefs.getString('statusDataArray');

      if (statusDataSerialzed != null && statusDataSerialzed.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(statusDataSerialzed);

        complaintStatusesModel = dataArray
            .map((json) => ComplaintStatusesModel.fromJson(json))
            .toList();

        // Update the dropdown lists if needed
        final updatedStatusList = <DropDownValueModel>[];
        complaintStatusesModel.forEach((status) {
          // Use the category id as the value and the name as the name
          // Check if the category id is 0 before adding to the list

          updatedStatusList.add(DropDownValueModel(
            name: status.name,
            value: status.id,
          ));
        });

        // print("Step 5: ${updatedStatusList}");

        setState(() {
          complaintStatus = updatedStatusList; // Update the status list
        });
      } else {
        print('No Status data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving category data from SharedPreferences: $e');
    }
  }

  Future<void> getLocation() async {
    Position position;
    try {
      position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        latitude = '${position.latitude}';
        longitude = '${position.longitude}';
      });
    } catch (e) {
      print("Error while getting location: $e");
    }
  }

//Post Compalint
  Future<void> postComplaintData() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    if (token.isEmpty) {
      print('Access token is empty');
      return;
    }
    print(token);

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    // Create a Random instance to generate a boundary
    var random = Random();
    var boundary = '---------------------------${random.nextInt(1000000000)}';

    // Set Content-Type with boundary parameter

    // Create a FormData object to send as the request body
    var formData = FormData.fromMap({
      'complaint_id': widget.userId.toString(),
      'status_id': _statusId.toString(),
      'progress': _progress.toString(),
      'description': _description.toString(),
      'latitude': latitude.toString(),
      'longitude': longitude.toString(),
      'attachments': await MultipartFile.fromFile(filePath),
    });

    // printSelectedValues();

    // Send the request using Dio (an HTTP client for Dart)
    var dio = Dio();
    var response = await dio.post(
      appBaseUrl + appUpdateComplaint,
      data: formData,
      options: Options(
        headers: headers,
      ),
    );

    print("Responce Data: ${response.data}");

    if (response.statusCode == 200 || response.statusCode == 201) {
      print("Data Upload Successfully....");

      showAnimatedCheckmarkDialog(
          context, 'Complaint Update Submitted!', appcolor);
      _isLoading = false;
      await Future.delayed(Duration(seconds: 1));

      final route = MaterialPageRoute(builder: (context) => Home());
      Navigator.pushAndRemoveUntil(context, route, (route) => false);
    } else {
      _isLoading = false;
      // Error handling

      print('API Error: ${response.statusCode}+${response.data}');

      // Show a simple dialog with the API error message
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: Text('Server Side Issue!'),
            children: <Widget>[
              SimpleDialogOption(
                onPressed: () {
                  Navigator.of(context).pop(); // Close the dialog
                },
                child: Text(
                    'Something Went Wrong! ' + response.statusCode.toString()),
              ),
            ],
          );
        },
      );
    }
  }

// Dialog fuction
  void showCustomDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(
            "Select Action!",
            textAlign: TextAlign.center,
          ),
          content: SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: appcolor,
                  ),
                  onPressed: () async {
                    String fPath = "";
                    String? imagePath = await useImageFromCamera();
                    setState(() {});
                    print("File Name: " + imagePath.toString());
                    if (imagePath != null) {
                      filePath = imagePath.toString();
                      Navigator.of(context).pop(); // Close the dialog
                    }

                    File imageFile = File(filePath);

                    try {
                      int fileSize4MB = (4 * 1024); //4MB

                      int fileSizeMB = imageFile.lengthSync(); // file length

                      if (fileSizeMB <= fileSize4MB) {
                        filePath = filePath;

                        print('File size: $filePath');
                      }
                    } catch (error) {
                      print('Upload error: $error');

                      // Show a simple dialog with the error message
                    }
                  },
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Take a Photo",
                        style: TextStyle(
                          color: dfColor,
                        ),
                      ),
                      Icon(
                        Icons.camera,
                        color: dfColor,
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 20),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: appcolor,
                  ),
                  onPressed: () async {
                    String fPath = "";
                    String? imagePath = await useImageFromGallery();
                    setState(() {});
                    print("File Name: " + imagePath.toString());
                    if (imagePath != null) {
                      filePath = imagePath.toString();
                      Navigator.of(context).pop(); // Close the dialog
                    }

                    File imageFile = File(filePath);

                    try {
                      int fileSize4MB = (4 * 1024); //4MB

                      int fileSizeMB = imageFile.lengthSync(); // file length

                      if (fileSizeMB <= fileSize4MB) {
                        filePath = filePath;

                        print('File size: $filePath');
                      }
                    } catch (error) {
                      print('Upload error: $error');

                      // Show a simple dialog with the error message
                    }
                  },
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Choose From Gallery",
                        style: TextStyle(
                          color: dfColor,
                        ),
                      ),
                      Icon(
                        Icons.photo_library_outlined,
                        color: dfColor,
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 10),
              ],
            ),
          ),
        );
      },
    );
  }

  //Image From Gallery
  Future<String?> useImageFromGallery() async {
    // Add code to open image picker and return the selected image path
    // For example, using the image_picker package
    final pickedImage =
        await ImagePicker().pickImage(source: ImageSource.gallery);
    if (pickedImage != null) {
      return pickedImage.path;
    }
    return null; // Return null if no image is selected
  }

  //Image From camera
  Future<String?> useImageFromCamera() async {
    // Add code to open image picker and return the selected image path
    // For example, using the image_picker package
    final pickedImage =
        await ImagePicker().pickImage(source: ImageSource.camera);
    print("Use Camera: ${pickedImage?.path.toString()}");
    if (pickedImage != null) {
      return pickedImage.path;
    }
    return null; // Return null if no image is selected
  }

// get Device Time
  void getCurrentTime() {
    final DateTime now = DateTime.now();
    final String formattedTime = "${now.hour}:${now.minute}:${now.second}";
    setState(() {
      currentTime = formattedTime;
    });
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    getStatusFromSharedPreferences();
    getLocation();
    print(widget.userId);
  }

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scheight = MediaQuery.of(context).size.height;
    return Scaffold(
      appBar: CustomAppBar(
          navFunction: () {
            Navigator.of(context).pop();
          },
          lastIcon: Icons.info_outline,
          infoFunction: () {
            CustomDialog(context);
          }),
      body: OverlayLoaderWithAppIcon(
        overlayBackgroundColor: appcolor,
        isLoading: _isLoading,

        appIcon: CircularProgressIndicator(),
        // appIcon: Image.asset(
        //   "asserts/icons/app_icon.png",
        //   width: 40,
        // ),
        child: Container(
          height: scheight,
          width: scWidth,
          color: drakGreyColor,
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  // color: appcolor,
                  width: scWidth,
                  alignment: Alignment.center,
                  margin: EdgeInsets.only(
                    bottom: marginLR,
                  ),
                  padding: EdgeInsets.only(top: 20, bottom: 0),
                  child: Text(
                    "Update Complaint",
                    style: TextStyle(
                      color: appcolor,
                      fontWeight: FontWeight.w600,
                      fontSize: lgFontSize,
                    ),
                  ),
                ),
                Container(
                  margin:
                      EdgeInsets.only(left: marginLR, right: marginLR, top: 10),
                  child: Form(
                    key: _formKey,
                    child: Stack(
                      children: [
                        Container(
                          margin: EdgeInsets.only(bottom: scheight / 10),
                          padding: EdgeInsets.all(marginLR),
                          // height: scheight / 2.5,
                          decoration: BoxDecoration(
                              color: dfColor,
                              borderRadius: BorderRadius.circular(15)),
                          child: SingleChildScrollView(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Container(
                                  margin: EdgeInsets.only(top: 8),
                                  child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          "Status",
                                          style: TextStyle(
                                              fontSize: exSmFontSize,
                                              fontWeight: FontWeight.w500,
                                              color: appcolor),
                                        ),
                                        DropDownTextField(
                                          // initialValue: "name4",
                                          // readOnly: true,
                                          controller: _cnt,
                                          clearOption: true,
                                          dropDownIconProperty: IconProperty(
                                              icon: Icons.keyboard_arrow_down),

                                          keyboardType: TextInputType.number,
                                          autovalidateMode:
                                              AutovalidateMode.disabled,
                                          clearIconProperty:
                                              IconProperty(color: Colors.green),

                                          validator: (value) {
                                            if (value!.isEmpty) {
                                              return "Please Select status";
                                            }
                                            return null;
                                          },
                                          // dropDownItemCount: 6,

                                          dropDownList: complaintStatus,
                                          onChanged: (value) {
                                            setState(() {
                                              _status = value.name;
                                              _statusId = value.value;

                                              print(
                                                  "Status Name: ${_status}, status id: ${_statusId}");
                                            });
                                          },
                                        ),
                                      ]),
                                ),

                                //------------------

                                Container(
                                  margin: EdgeInsets.only(top: 8),
                                  child: TextFormField(
                                    textInputAction: TextInputAction.next,
                                    autofocus: false,
                                    style: TextStyle(
                                        fontSize: 19.0, color: Colors.black87),
                                    decoration: InputDecoration(
                                      hintText: "Progress",
                                      hintStyle: TextStyle(
                                          color: Colors.black45, fontSize: 15),
                                      filled: true,
                                      fillColor: dfColor,
                                      contentPadding: const EdgeInsets.only(
                                          left: 1.0, bottom: 8.0, top: 8.0),
                                    ),
                                    validator: (value) {
                                      if (value == null || value.isEmpty) {
                                        return 'Please Write Progress';
                                      }

                                      final number = int.tryParse(value);
                                      if (number == null ||
                                          number < 1 ||
                                          number > 100) {
                                        return 'Please Enter a Number b/w 1 - 100';
                                      }

                                      return null;
                                    },
                                    keyboardType: TextInputType.number,
                                    maxLength: 3,
                                    inputFormatters: <TextInputFormatter>[
                                      FilteringTextInputFormatter.digitsOnly
                                    ],
                                    onChanged: (value) {
                                      setState(() {
                                        _progress = value.trim();

                                        print("Progress : ${_progress}");
                                      });
                                    },
                                  ),
                                ),

                                //------------------

                                Container(
                                  margin: EdgeInsets.only(top: 16),
                                  child: TextFormField(
                                    textInputAction: TextInputAction.next,
                                    autofocus: false,
                                    minLines: 1,
                                    maxLength: 500,
                                    maxLines: 5,
                                    style: TextStyle(
                                      fontSize: 19.0,
                                      color: Colors.black87,
                                    ),
                                    decoration: InputDecoration(
                                      hintText:
                                          "Type your complaint (Max 500 Characters)",
                                      hintStyle: TextStyle(
                                          color: Colors.black45, fontSize: 12),
                                      filled: true,
                                      fillColor: drakGreyColor,
                                      contentPadding: const EdgeInsets.only(
                                          left: 15.0,
                                          bottom: 30.0,
                                          top: 30.0,
                                          right: 15),
                                      focusedBorder: OutlineInputBorder(
                                        borderSide:
                                            BorderSide(color: Colors.white),
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      enabledBorder: UnderlineInputBorder(
                                        borderSide:
                                            BorderSide(color: Colors.white),
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                    ),
                                    keyboardType: TextInputType.text,
                                    inputFormatters: <TextInputFormatter>[
                                      FilteringTextInputFormatter.allow(
                                          RegExp(r'[a-zA-Z0-9. ]'))
                                    ],
                                    validator: (value) {
                                      if (value!.isEmpty) {
                                        return 'Please write your complaint';
                                      }

                                      // Define a regular expression pattern to match alphabets, numbers, and full stops
                                      final RegExp pattern =
                                          RegExp(r'^[a-zA-Z0-9. ]*$');

                                      if (!pattern.hasMatch(value)) {
                                        return 'Only alphabets, numbers, and full stops are allowed';
                                      }

                                      return null;
                                    },
                                    onChanged: (value) {
                                      setState(() {
                                        _description = value.trim();

                                        print("Description : ${_description}");
                                      });
                                    },
                                  ),
                                ),

                                //------------------

                                Container(
                                  margin: EdgeInsets.only(top: 10),
                                  child: CompalintImgCardWidget(
                                    onRemovePressed: () {
                                      // Handle the remove image action here

                                      setState(() {
                                        filePath = ''; // Set to empty string
                                      });
                                    },
                                    licenseImage: filePath,
                                    function: () {
                                      showCustomDialog(context);
                                    },
                                    imageText: 'Upload Image ',
                                    customImage: 'asserts/images/addstaff.png',
                                    ftSize: scWidth / 8,
                                  ),
                                ),

                                //-------------------
                              ],
                            ),
                          ),
                        ),
                        Positioned(
                          bottom: 0,
                          left: 0,
                          right: 0,
                          child: Container(
                            margin: EdgeInsets.only(
                              top: 10,
                            ),
                            decoration: BoxDecoration(
                                color:
                                    filePath.isEmpty ? lightappcolor : appcolor,
                                borderRadius: BorderRadius.circular(20)),
                            width: scWidth,
                            child: ElevatedButton(
                              onPressed: () async {
                                if (_formKey.currentState!.validate()) {
                                  getCurrentTime();
                                  bool internetConnected =
                                      await isInternetConnected();

                                  if (internetConnected) {
                                    setState(() {
                                      _isLoading = true;
                                    });

                                    if (filePath.isEmpty) {
                                      _isLoading = false;
                                      funToast("Image is Required", appcolor);
                                    } else {
                                      setState(() {
                                        _isLoading = true;
                                      });
                                      postComplaintData(); // Call your function to post the complaint
                                    }
                                  }
                                }
                              },
                              child: Text(
                                'Submit',
                                style: TextStyle(color: btnTextColor),
                              ),
                              style: ElevatedButton.styleFrom(
                                elevation: 0,
                                backgroundColor: Colors.transparent,
                                padding: EdgeInsets.symmetric(vertical: 12),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(roundBtn),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
