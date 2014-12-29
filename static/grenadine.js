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

  var activationPromise = function (pin) {
    return function () {
      var deferred = Q.defer()

      $.post('/pin/' + pin)
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

  _Control.activate = function (pin) {
    var args = Array.prototype.slice.call(arguments);
    console.debug("Queueing", args.length, "pin activations.", args);

    $.each(args, function (_,pin) {
      queue(activationPromise(pin));
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
