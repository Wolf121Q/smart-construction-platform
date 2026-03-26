import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/view_model/utils/date_formats.dart';
import 'package:flutter/material.dart';

class TrackDetail extends StatefulWidget {
  final String trackTime;
  final String trackRefNo;
  final String trackComplainStatus;
  final String category;
  final Color colorComplait;
  final String subCategory;
  final int index;

  const TrackDetail({
    required this.trackRefNo,
    required this.trackTime,
    required this.trackComplainStatus,
    required this.category,
    required this.subCategory,
    required this.colorComplait,
    required this.index,
  });

  @override
  State<TrackDetail> createState() => _TrackDetailState();
}

class _TrackDetailState extends State<TrackDetail> {
  bool isComplaitDetailVisible = false;

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return Container(
      alignment: Alignment.center,
      width: scWidth,
      margin: EdgeInsets.symmetric(vertical: marginLR, horizontal: 5),
      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 0),
      decoration: BoxDecoration(
          color: widget.colorComplait, borderRadius: BorderRadius.circular(12)),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Container(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  alignment: Alignment.center,
                  margin: EdgeInsets.only(bottom: marginSet + 2),
                  child: Text(
                    // textAlign: TextAlign.center,
                    widget.index.toString(),
                    style: TextStyle(
                      fontSize: exXSmFontSize,
                      fontWeight: FontWeight.bold,
                      color: appcolor,
                    ),
                    softWrap: true,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                Container(
                  margin: EdgeInsets.only(
                      left: marginLR + marginSet, bottom: marginSet),
                  alignment: Alignment.center,
                  width: scWidth / 1.5,
                  child: Text(
                    "Ref#: " + widget.trackRefNo,
                    style: TextStyle(
                      fontSize: smFontSize,
                      fontWeight: FontWeight.bold,
                      color: appcolor,
                    ),
                    softWrap: true,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                InkWell(
                  onTap: () {
                    if (isComplaitDetailVisible == false) {
                      isComplaitDetailVisible = true;
                    } else {
                      isComplaitDetailVisible = false;
                    }
                    setState(() {});
                  },
                  child: Material(
                    elevation: 3,
                    color: dfColor,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(180)),
                    child: Icon(
                      isComplaitDetailVisible == false
                          ? Icons.arrow_drop_down_sharp
                          : Icons.arrow_drop_up_sharp,
                      color: appcolor,
                      size: exLgFontSize + 5,
                    ),
                  ),
                ),
              ],
            ),
          ),
          Visibility(
            visible: isComplaitDetailVisible,
            child: Container(
              margin: EdgeInsets.symmetric(horizontal: 2, vertical: marginLR),
              child: Material(
                borderRadius: BorderRadius.circular(12),
                elevation: 1,
                child: AnimatedContainer(
                  duration: const Duration(seconds: 2),
                  curve: Curves.fastOutSlowIn,
                  padding: EdgeInsets.symmetric(
                      vertical: marginLR, horizontal: marginLR),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [],
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            textAlign: TextAlign.end,
                            "Category:",
                            style: TextStyle(
                              fontSize: exSmFontSize,
                              fontWeight: FontWeight.w600,
                              color: appcolor,
                            ),
                            softWrap: true,
                            overflow: TextOverflow.ellipsis,
                          ),
                          Text(
                            textAlign: TextAlign.end,
                            widget.category,
                            style: TextStyle(
                              fontSize: exSmFontSize,
                              fontWeight: FontWeight.w600,
                              color: appcolor,
                            ),
                            softWrap: true,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                      Container(
                        padding: EdgeInsets.only(top: marginSet + 3),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              textAlign: TextAlign.end,
                              "Sub Category:",
                              style: TextStyle(
                                fontSize: exSmFontSize,
                                fontWeight: FontWeight.w600,
                                color: appcolor,
                              ),
                              softWrap: true,
                              overflow: TextOverflow.ellipsis,
                            ),
                            Container(
                              width: scWidth / 2,
                              child: Text(
                                textAlign: TextAlign.end,
                                widget.subCategory,
                                style: TextStyle(
                                  fontSize: exSmFontSize,
                                  fontWeight: FontWeight.w600,
                                  color: appcolor,
                                ),
                                softWrap: true,
                                overflow: TextOverflow.ellipsis,
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
          ),
          Text(
            textAlign: TextAlign.center,
            formatDate(widget.trackTime),
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: appcolor,
            ),
          ),
        ],
      ),
    );
  }
}
