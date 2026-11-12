// Tema: clase, plantilla y estilos colaboran sin mezclar sus responsabilidades.
import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'demo-products',
  standalone: true,
  templateUrl: './after.html',
  styleUrl: './after.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProductsComponent {
  readonly products = [{ id: 1, name: 'Coffee' }, { id: 2, name: 'Tea' }];
}
