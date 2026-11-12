// Tema: el componente utiliza una capacidad que Angular le proporciona.
import { Component, Injectable, inject } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class PricingService {
  total(unitPrice: number, quantity: number): number {
    return unitPrice * quantity;
  }
}

@Component({ selector: 'demo-price', standalone: true, template: '{{ total }}' })
export class PriceComponent {
  private readonly pricing = inject(PricingService);
  readonly total = this.pricing.total(5, 2);
}
