// Single source of truth for the landing-page metrics strip.
// Update these values here, not inline in the component.

export interface Metric {
  value: string;
  label: string;
}

export const landingMetrics: Metric[] = [
  { value: '5',    label: 'projects shipped'   },
  { value: '33',   label: 'tests passing'      },
  { value: '75%',  label: 'ABQ on DABench'     },
  { value: '2027', label: 'graduating'         },
];
