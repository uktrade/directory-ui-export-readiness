'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const Server = require('karma').Server;
const PROJECT_DIR = path.resolve(__dirname);
const SASS_FILES = `${PROJECT_DIR}/core/sass/**/*.scss`;
const CSS_DIR = `${PROJECT_DIR}/core/static/styles`;
const CSS_FILES = `${PROJECT_DIR}/core/static/styles/**/*.css`;
const HTML_JS_FILES = [
  `${PROJECT_DIR}/article/templates/article/**/*.html`,
  `${PROJECT_DIR}/casestudy/templates/casestudy/**/*.html`,
  `${PROJECT_DIR}/core/templates/core/**/*.html`,
  `${PROJECT_DIR}/euexit/templates/euexit/**/*.html`,
  `${PROJECT_DIR}/finance/templates/finance/**/*.html`,
  `${PROJECT_DIR}/core/static/js/**/*.js`,
  `${PROJECT_DIR}/triage/static/js/**/*.js`,
  `${PROJECT_DIR}/article/static/js/**/*.js`,
];

// Run test once and exit
gulp.task('test', function (done) {
  new Server({
    configFile: __dirname + '/karma.conf.js',
    singleRun: true
  }, done).start();
});

gulp.task('purgecss', function() {
  return gulp.src(CSS_FILES)
    .pipe(purgecss({
      content: HTML_JS_FILES
    }))
    .pipe(gulp.dest(CSS_DIR));
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

gulp.task('sass:watch', function () {
  gulp.watch(
    [SASS_FILES],
    ['sass']
  );
});

gulp.task('default', ['sass']);
