var user_pick_list = [];

function toggle_list(clicked_id) {
        if(document.getElementById(clicked_id).className == "w-48 transition hover:scale-110 transform rounded-lg bg-white my-2 mx-2") {
                document.getElementById(clicked_id).className = "w-48 transition hover:scale-110 transform rounded-lg bg-blue-300 my-2 mx-2";
                user_pick_list.push(document.getElementById(clicked_id).id);
                console.log(user_pick_list);
        }
        else {
                document.getElementById(clicked_id).className = "w-48 transition hover:scale-110 transform rounded-lg bg-white my-2 mx-2";
                var index = user_pick_list.indexOf(document.getElementById(clicked_id).id);
                if (index !== -1) {
                        user_pick_list.splice(index, 1);
                }
                console.log(user_pick_list)
        }
}

function submit_list(button) {
        document.getElementById(button).value = user_pick_list;
}

// $(document).on('submit','#get_pick_form',function(e)
                //    {
//       console.log('hello');
//       e.preventDefault();
//       $.ajax({
        // type:'POST',
        // url:'/list_user/',
        // data:{
        //   todo:$("#data_button").value()
        // },
        // success:function()
        // {
        //   alert('saved');
        // }
//       })
//     });