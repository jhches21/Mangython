/* App Module */

var mangaApp = angular.module('mangaApp', [
  'ngAnimate',
  'ngSanitize',
  'ui.router',

  'headerControllers',
  'homeControllers'
]);

mangaApp.config(['$locationProvider', '$stateProvider', '$urlRouterProvider',
  function($locationProvider, $stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/');

    $stateProvider
      .state('app', {
        url: '/',
        views: {
          'header': {
            templateUrl: 'static/partials/header.html',
            controller: 'HeaderCtrl'
          },
          'content': {
            templateUrl: 'static/partials/home.html',
            controller: 'HomePageCtrl'
          }
        }
      })

      .state('app.hello', {
        url: 'hello',
        views: {
          'content@': {
            templateUrl: 'static/partials/hello.html'
          }
        }
      })

      .state('app.test', {
        url: 'test',
        views: {
          'content@': {
            templateUrl: 'static/partials/test.html'
          }
        }
      });

    $locationProvider.html5Mode(true);
  }]);

/* Directives */

mangaApp.directive('focusMe', function($timeout) {
  return {
    scope: { trigger: '=focusMe' },
    link: function(scope, element) {
      scope.$watch('trigger', function(val) {
        if(val) {
          $timeout(function() {
            element[0].focus();
            scope.trigger = false;
          });
        }
      });
    }
  };
});

mangaApp.directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        if (attrs.src != attrs.errSrc) {
          attrs.$set('src', attrs.errSrc);
        }
      });
    }
  };
});

mangaApp.directive('imageOnload', function() {
  return {
    restrict: 'A',
    scope: {
      execute: '&imageOnload'
    },
    link: function(scope, element, attrs) {
      element.bind('load', function() {
        scope.execute();
      });

      element.bind('error', function() {
        scope.execute();
      });
    }
  };
});

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
        }, 400);
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
        $scope.getAllSeries();
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
