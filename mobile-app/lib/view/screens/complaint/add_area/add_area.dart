import 'dart:convert';
import 'package:awesome_dialog/awesome_dialog.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/values_manager.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view/widgets/app_bar/custom_app_bar.dart';
import 'package:dha_ctt_app/view/widgets/custom_widgets/customs_widgets.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/alert_dialogs.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/area_hierarchy.dart';
import 'package:dotted_border/dotted_border.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AddAreaSelection extends StatefulWidget {
  @override
  _AddAreaSelectionState createState() => _AddAreaSelectionState();
}

class _AddAreaSelectionState extends State<AddAreaSelection> {
  TextEditingController _controller = TextEditingController();
  String selectedValue = '';
  final List<AreaHierarchy> selectedAreaList = [];
  int? areaId;

  List<AreaHierarchy> updatedAreaList = [];

  List<AreaHierarchy> areaHierarchy = [];
//
  Future<void> getAreaFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? serializedData = prefs.getString('areaHierarchy');

      if (serializedData != null && serializedData.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(serializedData);

        areaHierarchy =
            dataArray.map((json) => AreaHierarchy.fromJson(json)).toList();
        // Update the dropdown lists if needed
        List<AreaHierarchy> updateList = [];

        print("areaId old : ${areaId}");
        final SharedPreferences prefs = await SharedPreferences.getInstance();
        final int? user_area_type_id = prefs.getInt('user_area_type_id');
        if (selectedAreaList.isEmpty) {
          areaHierarchy.forEach((item) {
            if (item.id == user_area_type_id) {
              updateList.add(item);
              return;
            } else {
// updateList.add(areaHierarchy.first);
            }
          });

          // updateList.add(areaHierarchy.first);
        } else {
          areaHierarchy.forEach((item) {
            if (item.parent == areaId) {
              updateList.add(item);
            }
          });
        }

        setState(() {
          updatedAreaList = updateList; // Update the category dropdown list
        });
      } else {
        print('No area data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving category data from SharedPreferences: $e');
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();

    storeArealistApi();
    getAreaFromSharedPreferences();
    storeCategorieslistApi();
    storeQACategorieslistApi();
    setState(() {
      selectedAreaList;
    });
  }

  // int sideMarign = 0;

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      backgroundColor: drakGreyColor,
      appBar: CustomAppBar(
          navFunction: () {
            Get.back();
          },
          lastIcon: Icons.info_outline,
          infoFunction: () {
            CustomDialog(context);
          }),
      body: SafeArea(
        child: Container(
          margin: EdgeInsets.symmetric(horizontal: AppMargin.m20),
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
                padding: EdgeInsets.only(top: 15, bottom: 0),
                child: Text(
                  "Select Area",
                  style: TextStyle(
                    color: appcolor,
                    fontWeight: FontWeight.w700,
                    fontSize: lgFontSize,
                  ),
                ),
              ),
              Column(
                children: [
                  Container(
                    height: scHeight / 12,
                    width: scWidth,
                    child: Row(
                      children: [
                        Image.asset(
                          "asserts/gifs/marker_animation.gif",
                          color: appcolor,
                          width: AppSize.s30,
                        ),
                        SizedBox(width: 8),
                        Spacer(),
                        buildShimmerIcon(
                            updatedAreaList: updatedAreaList.isNotEmpty,
                            onPressed: () {
                              ////////////
// Call this function where you need to show the dialog od area seletion
                              showSearchDialog(
                                  context, updatedAreaList, _controller);
                              print("All Area List: ${updatedAreaList.length}");
                            }),
                      ],
                    ),
                  ),

                  /////// Selected area container ////////////
                  Container(
                    margin: EdgeInsets.only(bottom: marginLR, top: marginSet),
                    height: scHeight / 1.9,
                    width: scWidth,
                    child: Container(
                      height: scHeight / 1.6,
                      width: scWidth,
                      child: DottedBorder(
                        borderType: BorderType.RRect,
                        strokeWidth: 1,
                        radius: Radius.circular(roundCardView),
                        color: appcolor,
                        child: Container(
                          height: scHeight / 1.6,
                          child: Column(
                            // alignment: Alignment.center,
                            children: [
                              //Control background Image
                              areaId == null
                                  ? GestureDetector(
                                      onTap: () {
                                        // Call this function where you need to show the dialog add area seletion

                                        showSearchDialog(context,
                                            updatedAreaList, _controller);
                                      },
                                      child: Container(
                                        child: Opacity(
                                          opacity: 0.6,
                                          child: Image.asset(
                                            "asserts/images/noarea_selection.png",
                                          ),
                                        ),
                                      ),
                                    )
                                  : Container(
                                      height: scHeight / 2,
                                      padding: EdgeInsets.all(8),
                                      decoration: BoxDecoration(
                                        color: Colors.transparent,
                                      ),
                                      child: ListView.builder(
                                        itemCount: selectedAreaList.length,
                                        itemBuilder: (context, index) {
                                          int id = selectedAreaList[index].id;
                                          String name =
                                              selectedAreaList[index].name;

                                          double listsizer = 1.0;

                                          if (index == 0) listsizer = 1;
                                          if (index == 1) listsizer = 1.4;
                                          if (index == 2) listsizer = 1.6;
                                          if (index == 3) listsizer = 1.8;

                                          return Column(
                                            children: [
                                              Container(
                                                width: scWidth / listsizer,
                                                margin: EdgeInsets.only(
                                                  top: marginSet + marginSet,
                                                ),
                                                decoration: BoxDecoration(
                                                  color: appcolor,
                                                  borderRadius:
                                                      BorderRadius.circular(
                                                          roundCardView + 10),
                                                ),
                                                child: Container(
                                                    alignment: Alignment.center,
                                                    padding: EdgeInsets.all(
                                                        marginLR),

                                                    // alignment: Alignment.center,
                                                    child: Row(
                                                      mainAxisAlignment:
                                                          MainAxisAlignment
                                                              .spaceBetween,
                                                      children: [
                                                        Container(
                                                          width: scWidth /
                                                              marginLR,
                                                        ),
                                                        Container(
                                                          width: index == 0
                                                              ? scWidth / 2
                                                              : scWidth / 3.5,
                                                          child: Text(
                                                            '$name',
                                                            style: TextStyle(
                                                                fontWeight:
                                                                    FontWeight
                                                                        .bold,
                                                                color: dfColor,
                                                                fontSize:
                                                                    smFontSize),
                                                            softWrap: true,
                                                            overflow:
                                                                TextOverflow
                                                                    .visible,
                                                            textAlign: TextAlign
                                                                .center,
                                                          ),
                                                        ),
                                                        GestureDetector(
                                                          onTap: () {
                                                            setState(() {
                                                              removeItemsOnIndex(
                                                                  index);
                                                            });
                                                          },
                                                          child: SizedBox(
                                                            width: scWidth /
                                                                marginLR,
                                                            child: Icon(
                                                              Icons.close,
                                                              color: dfColor,
                                                              size: 25,
                                                            ),
                                                          ),
                                                        ),
                                                      ],
                                                    )),
                                              ),

                                              //Control the down arrow
                                              (index ==
                                                      selectedAreaList.length -
                                                          1)
                                                  ? Container()
                                                  : Image.asset(
                                                      "asserts/images/dropdown_polygon.png",
                                                      color: appcolor,
                                                      width: AppSize.s24,
                                                    ),

                                              if (index ==
                                                  selectedAreaList.length - 1)
                                                GestureDetector(
                                                  onTap: () {
                                                    // Call this function where you need to show the dialog add area seletion

                                                    showSearchDialog(
                                                        context,
                                                        updatedAreaList,
                                                        _controller);
                                                  },
                                                  child: Container(
                                                    margin:
                                                        EdgeInsets.symmetric(
                                                            vertical:
                                                                AppMargin.m20),
                                                    child: Image.asset(
                                                      updatedAreaList.isEmpty
                                                          // widget.updatedAreaList.isEmpty
                                                          ? "asserts/gifs/area_completed.gif"
                                                          : "asserts/gifs/add.gif",
                                                      //   color: appcolor,
                                                      width: AppSize.s60,
                                                    ),
                                                  ),
                                                ),
                                            ],
                                          );
                                        },
                                      ),
                                    ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),

                  /////// next btn ////////////
                  GestureDetector(
                    onTap: () {
                      if (areaId == null) {
                        CustomAlertDialog(
                          context,
                          title: "Info",
                          description: "Select Area First!",
                          dialogType: DialogType.info,
                          function: () {
                            // Navigator.of(context).pop();
                          },
                        );
                      } else {
                        showTwoSelectionDialog(
                          context,
                          selectedAreaList: updatedAreaList.isEmpty,
                          areaId: areaId == null ? 0 : areaId,
                        );
                      }
                    },
                    child: Container(
                      margin: EdgeInsets.only(top: AppMargin.m20),
                      width: scWidth,
                      decoration: BoxDecoration(
                        color: areaId == null ? applightcolor : appcolor,
                        borderRadius: BorderRadius.circular(30),
                      ),
                      padding: EdgeInsets.symmetric(
                          vertical: marginSet + 5,
                          horizontal: marginLR + marginLR),
                      alignment: Alignment.center,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Icon(
                            Icons.arrow_forward,
                            size: 0,
                            color: dfColor,
                          ),
                          Text(
                            'Next',
                            style: TextStyle(
                                color: dfColor,
                                fontSize: lgFontSize,
                                fontWeight: FontWeight.bold),
                          ),
                          Image.asset(
                            'asserts/gifs/arrow_forward.gif',
                            width: AppSize.s30,
                            color: dfColor,
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  void showSearchDialog(BuildContext context,
      List<AreaHierarchy> updatedAreaList, TextEditingController _controller) {
    if (updatedAreaList.isEmpty) {
      funToast("Area Selection Complete!", Colors.green);
    } else {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          // print("${selectedAreaList}");
          return Container(
            margin: EdgeInsets.only(top: 100, bottom: 100),
            child: Dialog(
              alignment: Alignment.topCenter,
              child: Container(
                padding: EdgeInsets.all(16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Visibility(
                      visible: false,
                      child: TextField(
                        controller: _controller,
                        decoration: InputDecoration(
                          labelText: 'Search',
                          hintText: 'Type to search...',
                          prefixIcon: Icon(Icons.search),
                          suffixIcon: _controller.text.isNotEmpty
                              ? GestureDetector(
                                  onTap: () {
                                    setState(() {
                                      _controller.clear();
                                      selectedValue = '';
                                      //  displayedOptions = updatedAreaList;

                                      print("Step ok: ${updatedAreaList}");
                                    });
                                  },
                                  child: Icon(Icons.clear),
                                )
                              : null,
                        ),
                        onChanged: (value) {
                          setState(() {});
                        },
                      ),
                    ),
                    ////////////////
                    Container(
                      margin: EdgeInsets.only(bottom: 10),
                      child: Text(
                        'Select Area',
                        style: TextStyle(
                            fontWeight: FontWeight.bold, fontSize: smFontSize),
                      ),
                    ),
                    Divider(
                      color: appcolor,
                    ),

                    SizedBox(height: 10),
                    Expanded(
                      child: updatedAreaList.isEmpty
                          ? Center(
                              child: Text('Item not found'),
                            )
                          : ListView.builder(
                              itemCount: updatedAreaList.length,
                              itemBuilder: (context, index) {
                                int id = updatedAreaList[index].id;
                                String name = updatedAreaList[index].name;
                                return ListTile(
                                  title: Text(
                                    '$name',
                                    style: TextStyle(
                                        fontWeight: FontWeight.w500,
                                        fontSize: dfFontSize),
                                  ),
                                  onTap: () {
                                    setState(() {
                                      selectedAreaList
                                          .add(updatedAreaList[index]);

                                      areaId = updatedAreaList[index].id;

                                      //////////----------/////
                                      print('tEST iD=' + areaId.toString());

                                      print('Area Size =' +
                                          updatedAreaList.length.toString());

                                      getAreaFromSharedPreferences();
                                    });
                                    Navigator.of(context)
                                        .pop(); // Close the dialog
                                  },
                                );
                              },
                            ),
                    ),
                    Container(
                      alignment: Alignment.centerRight,
                      child: ElevatedButton(
                        onPressed: () {
                          // Close the dialog without selecting any item
                          Navigator.of(context).pop();
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: appcolor,
                          elevation: 0,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(roundBtn),
                          ),
                        ),
                        child: Text('Close',
                            style: TextStyle(color: Colors.white)),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      );
    }
  }

  void removeItemsOnIndex(int index) {
    setState(() {
      areaId = (index > 0 && index <= selectedAreaList.length)
          ? selectedAreaList[index - 1].id
          : null;
      print('uodated area id = $areaId');
      selectedAreaList.removeRange(index, selectedAreaList.length);
      getAreaFromSharedPreferences();
    });
  }
}
