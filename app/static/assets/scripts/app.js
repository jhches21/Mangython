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
