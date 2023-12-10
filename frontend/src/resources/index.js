import {PLATFORM} from 'aurelia-pal';
export function configure(config) {
  config.globalResources([
    PLATFORM.moduleName('sc/propertylist'),
    //PLATFORM.moduleName('w3.css')
  ]);
}
