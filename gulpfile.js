'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const Server = require('karma').Server;
const del = require('del');

const PROJECT_DIR = path.resolve(__dirname);
const SASS_FILES = `${PROJECT_DIR}/core/sass/**/*.scss`;
const CSS_DIR = `${PROJECT_DIR}/core/static/styles`;
const CSS_FILES = `${PROJECT_DIR}/core/static/styles/**/*.css`;
const CSS_MAPS = `${PROJECT_DIR}/core/static/styles/**/*.css.map`;

// Run test once and exit
gulp.task('test', function (done) {
  new Server({
    configFile: __dirname + '/karma.conf.js',
    singleRun: true
  }, done).start();
});

gulp.task('clean', function() {
  return del([CSS_FILES, CSS_MAPS])
});

gulp.task('sass:compile', function () {
  return gulp.src(SASS_FILES)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        './conf/',
      ],
      outputStyle: 'compressed'
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest(CSS_DIR));
});

gulp.task('sass:watch', function () {
  gulp.watch(
    [SASS_FILES],
    ['sass:compile']
  );
});

gulp.task('sass', ['clean', 'sass:compile']);

gulp.task('default', ['sass']);
