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
