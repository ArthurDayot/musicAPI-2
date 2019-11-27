curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeColumn":"title","changeValueTo":"Test Update 1 to first inserted song", "artist": "Test artist 1","title":"Test Insert song 1"}' \
  http://127.0.0.1:5100/api/resources/tracks/update
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeColumn":"title","changeValueTo":"Test Update of title to song id = 4","id":4}' \
  http://127.0.0.1:5100/api/resources/tracks/update
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"changeColumn":"artist","changeValueTo":"Test Update of artist to song id = 5","id":5}' \
  http://127.0.0.1:5100/api/resources/tracks/update
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"id": 1, "hashed_password": "newpassword123"}' \
  http://127.0.0.1:5200/api/resources/users/update
curl \
  --header "Content-type: application/json" \
  --request PUT \
  --data '{"id": 2, "hashed_password": "anothernewpassword123"}' \
  http://127.0.0.1:5200/api/resources/users/update
