import 'package:dha_ctt_app/model/database/local_db.dart';
import 'package:dha_ctt_app/view_model/view_models/dashboard_model/dashboard_chat_model.dart';
import 'package:get/get.dart';
import 'package:get/get_state_manager/src/simple/get_controllers.dart';
import 'package:get_storage/get_storage.dart';

class DashboardChartController extends GetxController {
  var box = GetStorage();
  DashboardChatModel dashboardChatModel = DashboardChatModel();

  @override
  void onInit() {
    fetchData();
    // TODO: implement onInit
    super.onInit();
  }

  Future<void> fetchData() async {
    dashboardChatModel = await DBManager().fetchDashboardChart();

    await DBManager().fetchLoginUserEmail();
    print("======${await DBManager().fetchLoginUserEmail()}==========");

    update();
  }
}
