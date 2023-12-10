import environment from '../config/environment.json';
import { CustomElementRegistry } from 'aurelia-web-components';
import {PLATFORM} from 'aurelia-pal';

import { I18N,TCustomAttribute } from 'aurelia-i18n';
import Backend from 'i18next-xhr-backend';
//import resBundle from 'i18next-resource-store-loader!./locales/index.js'

export function configure(aurelia) {
  aurelia.use
    .standardConfiguration()
    .feature(PLATFORM.moduleName('resources/index'));

  aurelia.use.developmentLogging(environment.debug ? 'debug' : 'warn');

  if (environment.testing) {
    aurelia.use.plugin(PLATFORM.moduleName('aurelia-testing'));
  }

  aurelia.start().then(() => {
    const registry = aurelia.container.get(CustomElementRegistry);
    registry.fallbackPrefix = 'sc-';
    registry.forcePrefix = true;
    registry.useGlobalElements();
    //registry.register(Range);
  }); //aurelia.setRoot(PLATFORM.moduleName('app'))

}
