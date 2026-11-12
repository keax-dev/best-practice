// Tema: una regla potencialmente compartida queda dentro del componente.
import { Component } from '@angular/core';

@Component({ selector: 'demo-price-before', standalone: true, template: '{{ total }}' })
export class PriceBeforeComponent {
  readonly total = 5 * 2;
}
