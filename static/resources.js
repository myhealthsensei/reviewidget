// set up the angular module
angular.module('Resources', [])

// a slugifying filter
.filter('slugify', function () {
    var slugex = new RegExp('[^A-Za-z0-9-]+','g');
    return function (value) {
        return value.replace(slugex, '-').toLowerCase();
    }
})

// use [[ ]] to play nicely with django
.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    })

// edit controller
.controller('Edit', function ($scope, $http, $filter) {

    $scope.resource = {'id':false, 'public':false, 'logo':false};  // optional defaults

    $scope.filepicker = document.getElementById('file');

    $scope.add = function(){
        var f = document.getElementById('file').files[0],
        r = new FileReader();
        r.onloadend = function(e){
            $scope.resource.logo = e.target.result;
            $scope.$digest();
            }
        r.readAsBinaryString(f);
        }

    $scope.mkslug = function() {
        if (!$scope.resource.slug) { $scope.resource.slug = $filter('slugify')($scope.resource.name); };
        }

    $scope.save = function(resource) {
        console.log(resource);

        }

    })

