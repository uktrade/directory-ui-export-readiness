'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const Server = require('karma').Server;
const PROJECT_DIR = path.resolve(__dirname);
const SASS_FILES = `${PROJECT_DIR}/core/sass/**/*.scss`;
const PROTOTYPE_SASS_FILES = `${PROJECT_DIR}/prototype/sass/**/*.scss`;
const CSS_DIR = `${PROJECT_DIR}/core/static/styles`;

// Run test once and exit
gulp.task('test', function (done) {
  new Server({
    configFile: __dirname + '/karma.conf.js',
    singleRun: true
  }, done).start();
});

gulp.task('sass', function () {
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

gulp.task('sass:prototype', function () {
  return gulp.src(PROTOTYPE_SASS_FILES)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        './core/sass/',
      ],
      outputStyle: 'compressed'
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest(CSS_DIR));
});

gulp.task('sass:watch', function () {
  gulp.watch(
    [SASS_FILES, PROTOTYPE_SASS_FILES],
    ['sass', 'sass:prototype']
  );
});

gulp.task('default', ['sass', 'sass:prototype']);
