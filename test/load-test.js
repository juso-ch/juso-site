import http from 'k6/http';
import {sleep} from 'k6';

export default function() {
  http.get('http://213.167.224.189:9090');
  sleep(1);
}
