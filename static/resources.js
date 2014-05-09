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
        if (!$scope.resource.slug && $scope.resource.name) { $scope.resource.slug = $filter('slugify')($scope.resource.name); };
        }

    $scope.save = function(resource) {
        $http.post('/resources/', $scope.resource)
        .success( function (data) {
            console.log('OK', data);

            // make error tooltips
            if (data.errors) {
                // clear any old ones
                $('.popover').remove();

                for (i in data.errors) {
                    console.log(i,data.errors[i]);
                    $('#'+i).popover({
                        'show': true,
                        'placement': 'bottom',
                        'title': 'ERROR',
                        'content': data.errors[i],
                    });
                    $('#'+i).popover('show');
                }
            }

            // update with an ID or whatever the server may have changed
            $scope.resource = data;

        })
        .error( function (data) {
            console.log( 'NOT OK', data);
        })

    }

})

