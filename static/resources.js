// set up the angular module
angular.module('Resources', [])

// use [[ ]] to play nicely with django
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    })

// edit controller
.controller('Edit', function ($scope,$http) {

    $scope.resource = {'id':false, 'public':false};  // optional defaults

    $scope.add = function(){
        var f = document.getElementById('file').files[0],
        r = new FileReader();
        r.onloadend = function(e){
            $scope.resource.logo = e.target.result;
            }
        r.readAsBinaryString(f);
        }

    $scope.save = function(resource) {
        console.log(resource);

        }

    })

