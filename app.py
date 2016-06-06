import json
from flask import Flask, make_response, request
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

#our database :-)
users_database = list()

#index page
indexPage = """
<html>
<div>For get use GET,<br> for create use POST,<br> for update use PUT,<br> for del use DELETE</div><br>
<input  id='user_name' type="text" placeholder='input user name'>
<button id='get_btn'>GET</button>
<button id='post_btn'>POST</button>
<button id='put_btn'>PUT</button>
<button id='delete_btn'>DELETE</button><br><br>
<div id='room'></div>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-rc1/jquery.js'></script>
<script>
$(document).ready(function(){

		//method POST
        $('#post_btn').on('click', function(){

            //form data
            var user = {}
            user['name'] = $('#user_name').val();
			$('#user_name').val('')

            //send data via POST
            $.ajax({
                data: JSON.stringify(user),
                url: '/users',
                type: 'POST',
                contentType: 'application/json',
            })
        })

        //method GET
        $('#get_btn').on('click', function(){

            //recive data via GET
            $.ajax({
                url:'/users',
                type:'GET',
                dataType: 'json',
                success: function(reciveData) {
                    var i, data, parsed_data;

                    parsed_data = JSON.parse(reciveData);

                    //clear
                    $('#room').html('');
					data = '';

                    //insert parsed data
                    for(i=0; i<parsed_data.length; i++) {
                        data += '<li>' + parsed_data[i] + '</li>'
                    }
                    $('#room').html(data)
                }
            })
        })

        //method PUT
        $('#put_btn').on('click', function(){

            //form data
            var updated_user = {}
            updated_user['name'] = $('#user_name').val();
			$('#user_name').val('')

            //send data via PUT
            $.ajax({
                data: JSON.stringify(updated_user),
                url: '/users',
                type: 'PUT',
                contentType: 'application/json',
            })
        })

        //method DELETE
        $('#delete_btn').on('click', function(){

            //form data
            var deleted_user = {}
            deleted_user['name'] = $('#user_name').val();
			$('#user_name').val('')

            //send data via PUT
            $.ajax({
                data: JSON.stringify(deleted_user),
                url: '/users',
                type: 'DELETE',
                contentType: 'application/json',
            })
        })
})
</script>
</html>
"""

#index
class Index(Resource):
	headers = {'Content-Type':'text/html'}

	def get(self):
		return make_response(indexPage, 200, self.headers)

api.add_resource(Index, '/')

#users CRUD
class CRUD(Resource):
	headers = {'Content-Type':'application/json'}

	def get(self):
		#get all users
		return json.dumps(users_database)

	def post(self):
		user = request.get_json()
		if user['name'] not in users_database:
			#add (create) new user
			users_database.append(user['name'])
		return {'message': 'User already exist'}

	def put(self):
		user = request.get_json()
		if user['name'] in users_database:
			index = users_database.index(user['name'])
			#update user record
			users_database[index] += '_updated'
		return {'message': 'no such user in database'}

	def delete(self):
		user = request.get_json()
		if user['name'] in users_database:
			#remove user from database
			users_database.remove(user['name'])
		return {'message': 'no such user in database'}

api.add_resource(CRUD, '/users')


if __name__ == '__main__':
	app.run(port=5001)