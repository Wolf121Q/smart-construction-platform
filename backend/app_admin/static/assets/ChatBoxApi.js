
var ChatBoxApi = (function () {
    /*
     * Alias of this
     * @private
     */
    var self = {};
    /**
     * Sort an autocompletion result array with insensitivity to the case,
     * using the 1st elements (a[0] and b[0]) to process comparison
     * @public
     * @param {array} a
     * @param {array} b
     * @return {undefined}
     */

    //  admin/member/payment_schedule


    self.ShowImagePopup = function(url='')
    {       

        try {
                   newwindow=window.open(url,"Image",'height=320,width=420');
                   if (window.focus) {newwindow.focus()}
                   return false;

            }
        catch(e)
            {
                alert(e);
            }
    }


    self.task_action_flag_detail = function(id='')
    {       

        try {
                $("#modal_observation_detail").modal('show');

                var posturl = '/dashboard/projectdirectorhousing/task_action_flag_detail/';

                var retuntext           =   $.ajax({type: "POST",data:{'id':id}, url: posturl, async: false}).responseText;
                $("#modal_observation_detail_body").html(retuntext);

            }
        catch(e)
            {
                alert(e);
            }
    }
    
    self.task_action_first_attachment = function(id='')
    {       

        try {
                $("#modal_observation_detail").modal('show');

                var posturl = '/dashboard/projectdirectorhousing/task_action_first_attachment/';

                var retuntext           =   $.ajax({type: "POST",data:{'id':id}, url: posturl, async: false}).responseText;
                $("#modal_observation_detail_body").html(retuntext);

            }
        catch(e)
            {
                alert(e);
            }
    }


    self.LoadChatBox = function(id='')
    {       

        try {
               

                var posturl = '/dashboard/projectdirectorhousing/task_action_chat_detail/';

                var retuntext           =   $.ajax({type: "POST",data:{'id':id}, url: posturl, async: false}).responseText;
                $("#task_action_aside_support_body").html(retuntext);

                //retuntext = jQuery.parseJSON(retuntext);

                // if(retuntext.status == 1)
                // {
                //     var task_action = retuntext.data.task_action
                //     map = new OpenLayers.Map("map_osm_div");
                //     map.addLayer(new OpenLayers.Layer.OSM());

                //     var lonLat = new OpenLayers.LonLat( task_action.longitude,task_action.latitude  )
                //           .transform(
                //             new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
                //             map.getProjectionObject() // to Spherical Mercator Projection
                //           );
                          
                //     var zoom=16;

                //     var markers = new OpenLayers.Layer.Markers("Markers");
                //     map.addLayer(markers);

                //     markers.addMarker(new OpenLayers.Marker(lonLat));

                //     map.setCenter (lonLat, zoom);
                // }

            }
        catch(e)
            {
                alert(e);
            }
    }


    self.ShowChatBox = function(id='',title='')
    {       

        try {
               $("#task_action_id").val(id);
               $("#chatbox_title").html(title);
               $("#task_action_aside_support").modal('show');
               self.LoadChatBox(id);

                // var posturl = '/dashboard/projectdirectorhousing/task_action_flag_detail/';

                // var retuntext           =   $.ajax({type: "POST",data:{'id':id}, url: posturl, async: false}).responseText;

                // retuntext = jQuery.parseJSON(retuntext);

                // if(retuntext.status == 1)
                // {
                //     var task_action = retuntext.data.task_action
                //     map = new OpenLayers.Map("map_osm_div");
                //     map.addLayer(new OpenLayers.Layer.OSM());

                //     var lonLat = new OpenLayers.LonLat( task_action.longitude,task_action.latitude  )
                //           .transform(
                //             new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
                //             map.getProjectionObject() // to Spherical Mercator Projection
                //           );
                          
                //     var zoom=16;

                //     var markers = new OpenLayers.Layer.Markers("Markers");
                //     map.addLayer(markers);

                //     markers.addMarker(new OpenLayers.Marker(lonLat));

                //     map.setCenter (lonLat, zoom);
                // }

            }
        catch(e)
            {
                alert(e);
            }
    }

    self.ShowmOrganizationChartBox = function(id='')
    {       

        try {

            users_list = DashboardApi.getUsers();
            var options, index, select, option;
            // Get the raw DOM object for the select box
            select = document.getElementById('tag_user_id');
            // Clear the old options
            select.options.length = 0;
            // Load the new options
            options = users_list; // Or whatever source information you're working with
            for (index = 0; index < users_list.length; ++index) {
              option = options[index];
              select.options.add(new Option(option.full_name , option.value));
            }
            $("#modal_organization_chart").modal('show');

                // var posturl = '/dashboard/projectdirectorhousing/task_action_flag_detail/';

                // var retuntext           =   $.ajax({type: "POST",data:{'id':id}, url: posturl, async: false}).responseText;

                // retuntext = jQuery.parseJSON(retuntext);

                // if(retuntext.status == 1)
                // {
                //     var task_action = retuntext.data.task_action
                //     map = new OpenLayers.Map("map_osm_div");
                //     map.addLayer(new OpenLayers.Layer.OSM());

                //     var lonLat = new OpenLayers.LonLat( task_action.longitude,task_action.latitude  )
                //           .transform(
                //             new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
                //             map.getProjectionObject() // to Spherical Mercator Projection
                //           );
                          
                //     var zoom=16;

                //     var markers = new OpenLayers.Layer.Markers("Markers");
                //     map.addLayer(markers);

                //     markers.addMarker(new OpenLayers.Marker(lonLat));

                //     map.setCenter (lonLat, zoom);
                // }

            }
        catch(e)
            {
                alert(e);
            }
    }
    
    self.ShowmOrganizationChartBoxTemplate = function(id='')
    {       

        try {
            alert("CALLED")
            var posturl = '/dashboard/projectdirectorhousing/organization_hierarchy/';
            var retuntext           =   $.ajax({type: "GET",url: posturl, async: false}).responseText;
            $("#modal_organization_chart_body").html(retuntext);
            $("#modal_organization_chart").modal('show');

        }
        catch(e)
            {
                alert(e);
            }
    }

    // function getModelBox(task_action_comment_id = '', comment = '', remarks_by_tag = '', remark_date = '', flag_color =
    // '') {
    
    self.getTaskActionCommentId = function(id = '',tac_serial = ''){
        $(".parent-chat-div").each(function(){
            $( this ).removeClass("reply_bcg");
        })
        if(id != ''){
            $('#'+String('parent_div_'+String(tac_serial))).addClass("reply_bcg")
            $('#reply_id').val(id);
        }
    }
  
    self.ChatBoxOperation = function(id = '',){
        var reply_id = $('#reply_id').val();
        var task_action_id = $('#task_action_id').val();
        var comment_text = $('#commentTextbox').val();
        var attachment = $('#chat_attachment').val();
        var tagged_user_id = $("#tagged_user").val();

        if(comment_text != ""){
            // var fd = new FormData();
            // fd.append('attachment', attachment);
            // fd.append('task_action_id', task_action_id);
            // fd.append('reply_id', reply_id);
            // fd.append('comment_text', comment_text);
            // fd.append('tagged_user_id', tagged_user_id);
            $.ajax({
                url: '/dashboard/projectdirectorhousing/comment_reply/',
                dataType: "JSON",
                data: new FormData(document.querySelector("#action_comment_form")),
                method: 'POST',
                contentType: false,
                processData: false, // added data type
               success: function (res) {
                    //res = jQuery.parseJSON(res);
                    if(res.status == 1)
                    {
                        self.LoadChatBox(res.id); 
                        $('#comment_textbox').val('');
                        $('#reply_id').val('');
                        $("#tagged_user").val('');
                        $('#chat_attachment').val('')
                    }
                    //location.reload(true);
                }
            }); // new script code

        } 
        else {
            alert("Please Provide All Required Data")
        }
    }




 
 
    //     self.submitPaymentVoucherinfo = function()
//     {       

//         try {
//                 $.ajax({
//                     url: $('#payment_voucher_form').attr("action"),
//                     type: $('#payment_voucher_form').attr("method"),
//                     dataType: "JSON",
//                     data: new FormData(document.querySelector("#payment_voucher_form")),
//                     processData: false,
//                     contentType: false,
//                     success: function (data, status)
//                     {
//                        if(data.status == 1)
//                        {
//                             $("#submit_challan_info_btn").hide();
//                             $("#download_challan_pdf_btn").show();
//                             $("#main_payment_voucher_box").show();
//                             $("#generate_payment_voucher_box").hide();
//                        }

//                     },
//                     error: function (xhr, desc, err)
//                     {
//                         alert(data.data);

//                     }
//                 });        
//             }
//         catch(e)
//             {
//                 alert(e);
//             }
//     };

































    // self.fakePathRemover = function(file_name){
    //     var getFileName = file_name; 
    //     var changeFileName = getFileName.replace(/^.*[\\\/]/, '');
    //     return changeFileName;
    // }





    return self;
})();