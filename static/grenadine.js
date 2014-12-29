Grenadine = function(initialWait) {
  var timeoutPromise = function(time) {
    return function () {
      var deferred = Q.defer()

      setTimeout(function () {
        console.debug("Completed wait of", time, "milliseconds");
        deferred.resolve();
      }, time);

      return deferred.promise;
    }
  };

  var activatePromise = function (pin) {
    return function () {
      var deferred = Q.defer()

      console.debug("Activating", pin, ".")
      $.post('/pin/' + pin)
        .done(deferred.resolve)
        .fail(deferred.resolve);

      return deferred.promise;
    }
  };

  var deactivatePromise = function (pin) {
      return function () {
        var deferred = Q.defer()

        console.debug("Deactivating", pin, ".")
        $.delete('/pin/' + pin)
          .done(deferred.resolve)
          .fail(deferred.resolve);

        return deferred.promise;
      }
    };

  var clearingPromise = function () {
    return function () {
      var deferred = Q.defer()

      $.delete('/pins')
        .done(deferred.resolve)
        .fail(deferred.resolve);

      return deferred.promise;
    }
  };

  var _Control = {
    commands: [],
  };

  var queue = function (p) {
    _Control.commands.push(p);
  }

  _Control.wait = function (time) {
    queue(timeoutPromise(time));
    return this;
  };

  _Control.clear = function (time) {
    queue(clearingPromise(time));
    return this;
  };

  _Control.trigger = function (pin) {
    var args = Array.prototype.slice.call(arguments);

    $.each(args, function (_,pin) {
      queue(activatePromise(pin));
      queue(timeoutPromise(1000));
      queue(deactivatePromise(pin));
    });

    return this;
  };

  _Control.exec = function () {
    this.commands.reduce(Q.when, Q(true));
  }


  if (initialWait) {
    _Control.commands.push(timeoutPromise(initialWait));
  }

  return _Control;
}
