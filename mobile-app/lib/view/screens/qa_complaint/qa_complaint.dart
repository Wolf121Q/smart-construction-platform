import 'dart:io' show File, Platform;

import 'dart:math';
import 'package:connectivity/connectivity.dart';
import 'package:dha_ctt_app/animation/animated_checkmark_dialog.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/screens/pending_task/pending_task.dart';

import 'package:dha_ctt_app/view/widgets/app_bar/custom_app_bar.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/card_Image_widget.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';
import 'package:dha_ctt_app/view_model/view_models/qa_checklist/qa_checklist_model.dart';
import 'package:dio/dio.dart';

import 'package:dropdown_textfield/dropdown_textfield.dart';
import 'package:flutter/material.dart';
import 'package:overlay_loader_with_app_icon/overlay_loader_with_app_icon.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:geolocator/geolocator.dart';

import 'package:image_picker/image_picker.dart';


/// Flutter code sample for DropdownButton.

enum IdentityShift { Excellent, Good, Satisfactory, Poor, Very_Poor }

class QACheckList extends StatefulWidget {
  final int areaId;
  QACheckList({
    required this.areaId,
  });

  @override
  State<QACheckList> createState() => _QACheckListState();
}

class _QACheckListState extends State<QACheckList> {
  String appBaseUrl = AppStrings.appBaseUrl;
  String appQAchecklist = AppStrings.QA_CHECKLIST;
  String appGetQACategory = AppStrings.QA_GET_CATEGORY;
  // String appComplaintStatuses = AppStrings.COMPLAINT_STATUS;
  SingleValueDropDownController? _cnt;
  SingleValueDropDownController? _Subcnt;
  final _formKey = GlobalKey<FormState>();

  dynamic _category;
  dynamic _catID;
  dynamic _subcategory;
  dynamic _subCatID;
  dynamic _type;

  String _description = '';
  String _memberId = '';
  String _source = '';
  dynamic path = '';
  String? latitude;
  String? longitude;
  String? currentTime;
  List<DropDownValueModel> dropDownList = [];
  List<DropDownValueModel> subcategoryList = [];
  IdentityShift? _identityShift;
  String idenShift = '';

  int selectedCategory = 0;
  String filePath = '';
  bool _isLoading = false;

  dynamic _status;
  dynamic _statusId;

  late int _areaId = widget.areaId;

  int _progress = 0;
  int rating = 0;

  List<DropDownValueModel> complaintStatus = [];
  List<QAChecklistItem> chatagoriDataArray = [];

  Future<bool> isInternetConnected() async {
    var connectivityResult = await (Connectivity().checkConnectivity());
    return connectivityResult != ConnectivityResult.none;
  }

// Function to retrieve categories from SharedPreferences and populate the list
  Future<void> getCategoriesFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? serializedData = prefs.getString('qachatagoriDataArray');

      if (serializedData != null && serializedData.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(serializedData);

        chatagoriDataArray =
            dataArray.map((json) => QAChecklistItem.fromJson(json)).toList();

        // Update the dropdown lists if needed
        final updatedDropDownList = <DropDownValueModel>[];
        chatagoriDataArray.forEach((item) {
          // Use the category id as the value and the name as the name
          // Check if the category id is 0 before adding to the list

          if (item.mpttLevel == 0) {
            updatedDropDownList.add(DropDownValueModel(
              name: item.name,
              value: item.id,
            ));
          }
          // print("Step 2: ${updatedDropDownList}");
        });

        setState(() {
          dropDownList =
              updatedDropDownList; // Update the category dropdown list

          subcategoryList.clear();
          subcategoryList = [];
          //     selectedCategory); // Update the subcategory dropdown list
        });
      } else {
        print('No category data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving category data from SharedPreferences: $e');
    }
  }

  // getting Category ID
  Future<int?> getCategoryIdByName(String categoryName) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String storedData = prefs.getString('qachatagoriDataArray') ?? '';

    if (storedData.isNotEmpty) {
      final List<dynamic> dataArray = jsonDecode(storedData);

      print("Catewgory: " + dataArray.toString());

      for (var jsonData in dataArray) {
        final QAChecklistItem chatagoriData =
            QAChecklistItem.fromJson(jsonData);

        if (chatagoriData.name == categoryName) {
          selectedCategory = chatagoriData.id;
          print(chatagoriData.id);
          return chatagoriData.id;
        }
      }
    } else {
      print("storedData is Empty!");
    }

    return null; // Return null if category name is not found
  }

// Function to get subcategories by category ID
  List<DropDownValueModel> getSubcategoriesByCategoryId(
      List<QAChecklistItem> chatagoriDataArray, int categoryId) {
    List<DropDownValueModel> subcategories = [];

    for (var item in chatagoriDataArray) {
      if (item.parent == categoryId) {
        // Only add items with a category ID matching the selected category,
        // and exclude items with the same ID as the category (main category).
        subcategories.add(DropDownValueModel(
          name: item.name,
          value: item.id,
        ));
      }
    }
    print("Step 3: ${subcategories}");

    return subcategories;
  }

  Future<int?> getCategoryIdFromName(String categoryName) async {
    final prefs = await SharedPreferences.getInstance();
    final storedData = prefs.getString('chatagoriDataArray');

    if (storedData != null) {
      final List<dynamic> dataArray = jsonDecode(storedData);

      for (var jsonData in dataArray) {
        final QAChecklistItem chatagoriData =
            QAChecklistItem.fromJson(jsonData);

        if (chatagoriData.name == categoryName) {
          return chatagoriData.id;
        }
      }
    }
    //("this is comming from shared pref: " + chatagoriData.id.toString());
    return null; // Return null if category name is not found
  }

  //Get Complaint submittime id for uploading file.
  int extractIdFromApiResponse(String responseBody) {
    Map<String, dynamic> responseJson = json.decode(responseBody);
    print(responseJson);

    if (responseJson.containsKey("data")) {
      Map<String, dynamic> dataArray = responseJson["data"];
      if (dataArray.containsKey("id")) {
        int id = dataArray["id"];
        return id;
      }
    }

    // Return a default value or handle the case when id is not found
    return -1; // You can choose a suitable default value or error indicator
  }

  //Store local complaints
  Future<void> enqueueComplaint(Map<String, dynamic> complaint) async {
    final prefs = await SharedPreferences.getInstance();
    final List<String> queuedComplaints =
        prefs.getStringList('queued_complaints') ?? [];
    queuedComplaints.add(jsonEncode(complaint));
    await prefs.setStringList('queued_complaints', queuedComplaints);
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => PendingTask()));
  }

  Future<void> postQAComplaintData() async {
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
    headers['Content-Type'] = 'multipart/form-data; boundary=$boundary';

    // Create a FormData object to send as the request body
    var formData = FormData.fromMap({
      // 'status_id': _statusId.toString(),
      // 'subcategory_id': _subCatID.toString(),
      'category_id': _subCatID.toString(),
      'area_id': _areaId.toString(),
      'rating': rating.toString(),
      'latitude': latitude.toString(),
      'longitude': longitude.toString(),
      'attachments': await MultipartFile.fromFile(filePath),
    });

    printSelectedValues();

    // Send the request using Dio (an HTTP client for Dart)
    var dio = Dio();
    var response = await dio.post(
      appBaseUrl + appQAchecklist,
      data: formData,
      options: Options(
        headers: headers,
      ),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      print("Data Upload Successfully....");
      // final responseData = response.data;
      // Map<String, dynamic> responseJson = json.decode(responseData);

      // print("Responce Json: ${responseJson}");

      showAnimatedCheckmarkDialog(context, 'Complaint Registered!', appcolor);
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
    print("Use gallery: ${pickedImage?.path.toString()}");
    if (pickedImage != null) {
      return pickedImage.path;
    }
    return null; // Return null if no image is selected
  }

  //Image From Camera
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

//submitting
  void printSelectedValues() async {
    print("Selected Category: $_catID");
    print("Selected Subcategory: $_subCatID");
    // print("Selected Status: $_statusId");
    print("Selected Area: ${widget.areaId}");
    // print("Selected Description: $_description");
    // print("Selected Progress: ${_progress}");
    print("Selected latitude: ${latitude}");
    print("Selected longitude: ${longitude}");
    print("Selected longitude: ${filePath}");
  }

  void Rating(String rate) {
    if (rate.toLowerCase() == "excellent") {
      rating = 5;
      print(rate);
    } else if (rate.toLowerCase() == "good") {
      rating = 4;
      print(rate);
    } else if (rate.toLowerCase() == "satisfactory") {
      rating = 3;
      print(rate);
    } else if (rate.toLowerCase() == "poor") {
      rating = 2;
      print(rate);
    } else if (rate.toLowerCase() == "very poor") {
      rating = 1;
      print(rate);
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

  @override
  void initState() {
    super.initState();
    getCategoriesFromSharedPreferences();
    // storeCategorieslistApi();
    getLocation();
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
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
        appIcon: Image.asset(
          "asserts/icons/app_icon.png",
          width: 40,
        ),
        child: Container(
          height: scheight,
          width: scWidth,
          color: drakGreyColor,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              SingleChildScrollView(
                child: Container(
                  // color: appcolor,
                  width: scWidth,
                  alignment: Alignment.center,
                  margin: EdgeInsets.only(
                    bottom: marginLR,
                  ),
                  padding: EdgeInsets.only(top: 20, bottom: 0),
                  child: Text(
                    "QA Checklist",
                    style: TextStyle(
                      color: appcolor,
                      fontWeight: FontWeight.w600,
                      fontSize: lgFontSize,
                    ),
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
                        padding: Platform.isAndroid
                            ? EdgeInsets.only(
                                top: scheight / 1000 * 2,
                                right: 20,
                                left: 20,
                                bottom: scheight / 180)
                            : EdgeInsets.all(marginLR),
                        // height: scheight / 2.1,
                        decoration: BoxDecoration(
                            color: dfColor,
                            borderRadius: BorderRadius.circular(15)),
                        child: SingleChildScrollView(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Container(
                                margin: EdgeInsets.only(top: scheight / 100),
                                child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        "Category",
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
                                            return "Please Select Category";
                                          }
                                          return null;
                                        },
                                        // dropDownItemCount: 6,

                                        dropDownList: dropDownList,
                                        onChanged: (value) {
                                          _Subcnt =
                                              SingleValueDropDownController();
                                          setState(() {
                                            _category = value.name;
                                            _catID = value.value;

                                            print(
                                                "Cat Name: ${_category}, cat id: ${_catID}");
                                          });

                                          getCategoryIdByName(
                                                  _category.toString())
                                              .then((categoryId) {
                                            if (categoryId != null) {
                                              _catID = categoryId;
                                              setState(() {
                                                selectedCategory = categoryId;
                                                subcategoryList.clear();
                                                _subcategory = null;
                                                _Subcnt =
                                                    SingleValueDropDownController();
                                                subcategoryList =
                                                    getSubcategoriesByCategoryId(
                                                        chatagoriDataArray,
                                                        selectedCategory);
                                              });
                                            } else {
                                              // Handle the case when the category is not found
                                              print("Category not found.");
                                            }
                                          });
                                        },
                                      ),
                                    ]),
                              ),

                              //------------------

                              Container(
                                margin: EdgeInsets.only(top: scheight / 100),
                                child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        "Sub Category",
                                        style: TextStyle(
                                            fontSize: exSmFontSize,
                                            fontWeight: FontWeight.w500,
                                            color: appcolor),
                                      ),
                                      DropDownTextField(
                                        // initialValue: "name4",
                                        // readOnly: true,
                                        controller: _Subcnt,
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
                                            return "Please Select Sub Category";
                                          }
                                          return null;
                                        },
                                        // dropDownItemCount: 6,

                                        dropDownList: subcategoryList,
                                        onChanged: (value) {
                                          setState(() {
                                            _subcategory = value.name;
                                            _subCatID = value.value;

                                            print(
                                                "SubCat Name: ${_subcategory}, Subcat id: ${_subCatID}");
                                          });
                                        },
                                      ),
                                    ]),
                              ),

                              //------------------

                              Container(
                                height: scheight / 4.6,
                                margin: EdgeInsets.only(top: scheight / 100),
                                child: Column(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  children: [
                                    buildRadioWithProgress(
                                        IdentityShift.Excellent,
                                        "Excellent",
                                        1.0),
                                    buildRadioWithProgress(
                                        IdentityShift.Good, "Good", 0.8),
                                    buildRadioWithProgress(
                                        IdentityShift.Satisfactory,
                                        "Satisfactory",
                                        0.6),
                                    buildRadioWithProgress(
                                        IdentityShift.Poor, "Poor", 0.4),
                                    buildRadioWithProgress(
                                        IdentityShift.Very_Poor,
                                        "Very Poor",
                                        0.2),
                                  ],
                                ),
                              ),
                              //-------------------

                              Container(
                                margin: EdgeInsets.only(
                                    top: scheight / 100, bottom: 0),
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
                                  imageText: 'Upload Image',
                                  customImage: 'asserts/images/addstaff.png',
                                  ftSize: Platform.isAndroid
                                      ? scWidth / 8
                                      : scWidth / 8,
                                ),
                              ),

                              //---------------------
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
                              // gradient: lgBlue,
                              color:
                                  filePath.isEmpty ? lightappcolor : appcolor,
                              borderRadius: BorderRadius.circular(20)),
                          width: scWidth,
                          child: ElevatedButton(
                            onPressed: () async {
                              if (_formKey.currentState!.validate()) {
                                Rating(idenShift);

                                Random random = Random();

                                int randomId = random.nextInt(1000);

                                print("Rondom Id :" + randomId.toString());
                                Map<String, dynamic> complaintData = {
                                  'tagId': randomId,
                                  'tag': "QA_complaint",
                                  'category_id': _catID.toString(),
                                  'subcategory_id': _subCatID.toString(),
                                  'area_id': _areaId.toString(),
                                  'rating': rating.toString(),
                                  'latitude': latitude.toString(),
                                  'longitude': longitude.toString(),
                                  'attachments': filePath,
                                };

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
                                    postQAComplaintData(); // Call your function to post the complaint
                                  }
                                } else {
                                  if (filePath.isEmpty) {
                                    _isLoading = false;
                                    funToast("Image is Required", appcolor);
                                  } else {
                                    setState(() {
                                      _isLoading = true;
                                    });
                                    await enqueueComplaint(
                                        complaintData); // Call your function to post the complaint
                                  }

                                  // showAnimatedCheckmarkDialog(
                                  //     context,
                                  //     'No internet connectivity!\nComplaint Stored in Pending Task!',
                                  //     appcolor);
                                  // _isLoading = false;
                                  // await Future.delayed(Duration(seconds: 1));

                                  print(
                                      'No internet connectivity. Complaint enqueued.');

                                  // Navigate to the dashboard
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
    );
  }

  Widget buildRadioWithProgress(
      IdentityShift value, String label, double progress) {
    return Stack(
      children: [
        Row(
          children: [
            Radio<IdentityShift>(
              activeColor: appcolor,
              value: value,
              groupValue: _identityShift,
              visualDensity: const VisualDensity(
                horizontal: VisualDensity.minimumDensity,
                vertical: VisualDensity.minimumDensity,
              ),
              materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
              onChanged: (IdentityShift? radioValue) {
                setState(() {
                  _identityShift = radioValue;
                  idenShift = label;
                  print(idenShift);
                });
              },
            ),
            SizedBox(
              width: 10,
            ),
            Text(
              label,
              style: TextStyle(
                fontSize: dfFontSize,
                fontWeight: FontWeight.w600,
                color: appcolor,
              ),
            ),
          ],
        ),
        Positioned.fill(
          child: Align(
            alignment: Alignment.centerRight,
            child: Container(
              width: MediaQuery.of(context).size.width / 2.5,
              child: LinearProgressIndicator(
                value: progress,
                minHeight: 8,
                backgroundColor: Colors.grey,
                valueColor: AlwaysStoppedAnimation<Color>(appcolor),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
