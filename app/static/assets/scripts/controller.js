/* Controllers */

var headerControllers = angular.module('headerControllers', []);

headerControllers.controller('HeaderCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.accessible = false;
    $scope.permission = false;
    $scope.notFound = false;
    $scope.error = false;

    $scope.dir = '';

    $http.get('/dir-accessible')
    .success(function(data, status, headers, config) {
      if(data.error) {
        $scope.error = true;
        $scope.dir = data.dir;

        if(data.error === 'accessible') { $scope.accessible = true; }
        if(data.error === 'permission') { $scope.permission = true; }
        if(data.error === 'notFound') { $scope.notFound = true; }
      }
    }).error(function(data, status, headers, config) {

    });
  }]);

var homeControllers = angular.module('homeControllers', []);

homeControllers.controller('HomePageCtrl', ['$scope', '$http', '$timeout', '$sanitize',
  function($scope, $http, $timeout, $sanitize) {
    $scope.imageNotFound = false;
    $scope.seriesInfo = {};

    $scope.closeAll = function() {
      $scope.showSearch = false;
      $scope.showSearchSpinner = false;
      $scope.showSearchResult = false;
      $scope.showSeriesInfo = false;
    };

    $scope.getAllSeries = function() {
      $http.get('/get-series')
      .success(function(data, status, headers, config) {
        if(data.length > 0) {
          console.log(data);
          $scope.series = data;
        }
      }).error(function(data, status, headers, config) {

      });
    };

    $scope.closeAll();
    $scope.getAllSeries();

    $scope.searchManga = function() {
      searchTerm = $scope.searchTerm;

      if(searchTerm !== "" && searchTerm !== undefined) {
        $scope.showSearchSpinner = true;
        $scope.showSearchResult = false;
        $scope.showSeriesInfo = false;

        $scope.seriesInfo.url = '';

        // TODO: Search site by site.
        $http.get('/search')
        .success(function(data, status, headers, config) {

          $http.get('/search/' + searchTerm)
          .success(function(data, status, headers, config) {
            $scope.showSearchSpinner = false;
            $scope.showSearchResult = true;

            $scope.searchResult = data;
          }).error(function(data, status, headers, config) {
            console.log('error on searching for manga');
          });
        }).error(function(data, status, headers, config) {

        });
      }
    };

    $scope.getSeriesInfo = function(url, title, site) {
      if(url !== $scope.seriesInfo.url) {
        $scope.showSeriesInfo = false;

        $timeout(function() {
          $scope.seriesInfo.img = '';

          $http.post('/series-info', {site: site, url: url})
          .success(function(data, status, headers, config) {
            data.title = title;
            data.url = url;
            data.site = site;
            $scope.seriesInfo = data;
          }).error(function(data, status, headers, config) {

          });
        }, 410);
      }
    };

    $scope.addSeries = function() {
      // TODO: Check if series already exists
      var data = $scope.seriesInfo;

      seriesInfo = {
        name: data.title,
        url: data.url,
        site: data.site,
        imgUrl: data.img
      };

      $http.post('/add-series', seriesInfo)
      .success(function(data, status, headers, config) {
        console.log(data);
        $scope.series.push(data)
      }).error(function(data, status, headers, config) {

      });
    };

    $scope.showSeriesInfoOn = function() {
      $scope.$apply(function() {
        $scope.showSeriesInfo = true;
      });
    };

    $scope.setImageNotFound = function() {

    };
  }]);
