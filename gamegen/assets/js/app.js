import * as $ from 'jquery';

window.$ = $;
window.jQuery = $;


import 'bootstrap';

import '../css/app.scss'

import 'select2';
import 'select2/dist/css/select2.css';


$(() => {
  $('.select2-enable').select2();
});

import 'htmx.org';
window.htmx = require('htmx.org');


