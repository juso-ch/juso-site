/*******************************
 *           Set-up
 *******************************/

var
  gulp   = require('gulp'),

  // read user config to know what task to load
  config = require('./style/tasks/config/user')
;


/*******************************
 *            Tasks
 *******************************/

require('./style/tasks/collections/build')(gulp);
require('./style/tasks/collections/install')(gulp);

gulp.task('default', gulp.series('watch'));

/*--------------
      Docs
---------------*/

require('./style/tasks/collections/docs')(gulp);

/*--------------
      RTL
---------------*/

if (config.rtl) {
  require('./style/tasks/collections/rtl')(gulp);
}
