/***
 * RPG javascript library
 * Author: Jeff (jdost)
 *
 * This is a simple javascript wrapping library that handles the request/response
 * structure of the API for the RPG webapp.  It is meant to serve as both an
 * example in how to work with the API as well as an introductory aid in building
 * a webapp around the backend API.
 ***/
(function (lib) {
  if (typeof lib !== 'Object') {
    lib = {};
  }

  var prefix = lib.prefix || '',
    jQuery = window.jQuery || false,

    ready = false,
    routes,
    queue = []; // Queues up requests while waiting for the initial route request


  var ajax = function (args) {
    if (!args) { return false; }

    if (jQuery) { // If jQuery is available, use it to perform the ajax request
      return jQuery.ajax(args);
    }
  };

  var callbacks = {},
  /**
  Events that this library will 'trigger' and the user can 'bind' to.  Mostly useful
  for the async callbacks.
   **/
    events = {
      REGISTER: 'userRegistered',
      REGISTRATION_FAILED: 'failedRegistration',
      LOGIN: 'userLoggedIn',
      LOGIN_FAILED: 'failedLogin',
      LOGOUT: 'userLoggedOut'
    };

  lib.EVENTS = events;
  for (e in events) { // makes the events externally visible and initializes the
      // callback array
    if (hasOwnProperty(events, e)) {
      callbacks[events[e]] = [];
      lib.EVENTS[e] = events[e];
    }
  }

  // bind: pseudo event binding, just stores the callback function in an array
  lib.bind = function (evt, callback) {
    if (!callbacks[evt]) { return; } // Not a valid event
    callbacks[evt].push(callback);
  };
  // trigger: pseudo event triggering, just calls all of the stored callbacks
  lib.trigger = function (evt, args) {
    if (!callbacks[evt]) { return; } // Not a valid event
    for (func in callbacks[evt]) {
      func(args);
    }
  };

  if (jQuery) {
    // If jQuery is available, it will be used in ajax requests, setup a prefilter
    jQuery.ajaxPrefilter(function (options) {
      options.url = prefix + options.url;
      options.dataType = 'json';
    });
  }

  /** register:
      args: username - (string) username to register
            password - (string) password for this username to authenticate with

    Tries to register the user with the application, will trigger a REGISTERED event
    if the request succeeds, otherwise will trigger a REGISTRATION_FAILED event.

    NOTE: maybe should trigger a LOGIN event instead/additionally to the REGISTERED
    event
   **/
  lib.register = function (credentials) {
    if (!credentials.username || !credentials.password) {
      return;
    }
    if (!ready) { return queue.push(function () { lib.register(credentials); }); }

    ajax({
      url: routes.register,
      data: credentials,
      success: function (data) {
        lib.trigger(events.REGISTER);
      },
      statusCode: {
        409: function () { lib.trigger(events.REGISTRATION_FAILED); }
      }
    });
  };

  /** login
      args: username - (string) username to login with (should be registered)
            password - (string) password to login with (set during registration)

    Attempts to login with the provided username//password combination.  If the
    attempt is successful, will trigger a LOGIN event, if the attempt fails, a
    LOGIN_FAILED event will be triggered.
   **/
  lib.login = function (credentials) {
    if (!credentials.username || !credentials.password) {
      return;
    }
    if (!ready) { return queue.push(function () { lib.login(credentials); }); }

    ajax({
      url: routes.login,
      data: credentials,
      success: function (data) {
        lib.trigger(events.LOGIN);
      },
      statusCode: {
        400: function () { lib.trigger(events.LOGIN_FAILED); }
      }
    });
  };


  ajax({ // Has to request the endpoints from the API server
    url: '/',
    success: function (data) {
      routes = data;
      ready = true;
      if (queue.length) { // If there are any requests queued up, make them now
        for (var i = queue.length; i > 0; i--) {
          (queue.pop())();
        }
      }
    }
  });
}(window.rpg));
