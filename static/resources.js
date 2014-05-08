// set up the angular module
angular.module('Resources', [])

// use [[ ]] to play nicely with django
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    })

// edit controller
.controller('Edit', function ($scope,$http) {

    $scope.resource = {'id':false};  // optional

    $scope.save = function(resource) {
        console.log(resource);

        }

    })

