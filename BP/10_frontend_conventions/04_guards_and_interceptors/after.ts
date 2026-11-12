// Tema: la navegación y el envío del token tienen responsabilidades distintas.
import { Injectable, inject, signal } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { HttpInterceptorFn } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class SessionService {
  readonly token = signal<string | null>(null);
}

export const authGuard: CanActivateFn = () =>
  !!inject(SessionService).token() || inject(Router).createUrlTree(['/login']);

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const token = inject(SessionService).token();
  const belongsToApi = request.url.startsWith('/api/v1/');
  const isLogin = request.url === '/api/v1/auth/login';
  if (!belongsToApi || isLogin || !token) return next(request);
  return next(request.clone({ setHeaders: { Authorization: `Bearer ${token}` } }));
};
