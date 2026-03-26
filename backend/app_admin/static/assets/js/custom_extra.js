
var CustomExtra = (function () {
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

    self.getPopup = function (url) {
        try {
            newwindow = window.open(url, 'liveMatches', 'directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,height=1000,width=1000');
            if (window.focus) { newwindow.focus() }
            return false;
        }
        catch (e) {
            alert(e);
        }
    };

    self.change_member_env_list = function () {
        try {
            var member_id = $("#id_member_env_list").find(":selected").val();
            //alert(member_id);
            var url = "/membership/update_member_info/" + member_id + "/";
            window.location.href = url;
        }
        catch (e) {
            alert(e);
        }
    };


    return self;
})();
