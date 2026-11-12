// Tema: comprobar inyección, navegación y alcance del token sin un servidor real.
import '@angular/compiler';
import test from 'node:test';
import assert from 'node:assert/strict';
import { Injector, runInInjectionContext } from '@angular/core';
import { DefaultUrlSerializer, Router } from '@angular/router';
import { HttpRequest, HttpResponse } from '@angular/common/http';
import { firstValueFrom, of } from 'rxjs';
import { PriceComponent, PricingService } from '../dist/03_services_and_injection/after.js';
import { ProductsComponent } from '../dist/02_component_structure/after.js';
import { SessionService, authGuard, authInterceptor } from '../dist/04_guards_and_interceptors/after.js';

test('the component uses the pricing dependency supplied by the injector', () => {
  const injector = Injector.create({ providers: [PricingService] });
  const component = runInInjectionContext(injector, () => new PriceComponent());
  assert.equal(component.total, 10);
  assert.deepEqual(new ProductsComponent().products.map(product => product.id), [1, 2]);
});

test('an anonymous navigation redirects and a session permits navigation', () => {
  const session = new SessionService();
  const serializer = new DefaultUrlSerializer();
  const injector = Injector.create({ providers: [
    { provide: SessionService, useValue: session },
    { provide: Router, useValue: { createUrlTree: () => serializer.parse('/login') } },
  ] });
  const result = runInInjectionContext(injector, () => authGuard({}, {}));
  assert.equal(serializer.serialize(result), '/login');
  session.token.set('demo-only-not-a-jwt');
  assert.equal(runInInjectionContext(injector, () => authGuard({}, {})), true);
});

test('the interceptor attaches a credential only to permitted API requests', async () => {
  const session = new SessionService();
  session.token.set('demo-only-not-a-jwt');
  const injector = Injector.create({ providers: [{ provide: SessionService, useValue: session }] });
  for (const [url, expected] of [
    ['/api/v1/orders', 'Bearer demo-only-not-a-jwt'],
    ['/api/v1/auth/login', null], ['/api/v10/orders', null], ['https://example.com/api/v1/orders', null],
  ]) {
    let received;
    const response = runInInjectionContext(injector, () => authInterceptor(new HttpRequest('GET', url), request => {
      received = request;
      return of(new HttpResponse({ status: 200 }));
    }));
    await firstValueFrom(response);
    assert.equal(received.headers.get('Authorization'), expected);
  }
});
