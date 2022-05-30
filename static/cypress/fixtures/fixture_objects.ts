import type { StaticResponse } from "cypress/types/net-stubbing";
import type { Task } from "../../src/api/models/Task";

export const task: Task = {
  id: "ecg-qrs-classification-physiodb",
  description: "Labeling the QRS complex of Physionet ECGs",
  labels: [
    "Atrial fibrillation",
    "Normal sinus rhythm",
    "Ventricular tachycardia",
    "Noise",
    "Other",
  ],
};

export const allTasks: Task[] = [task];

export const nextImage: StaticResponse = {
  body: "sloth.jpg",
  headers: {
    "Content-Type": "text/plain",
  },
};

export const accessToken =
  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJmdWxsbmFtZSI6IlByb2YuIERyLiBGb2xpdm9yYSIsImV4cGlyZXMiOjMyMjg1NzY2ODEuNjkxNjMxM30.feRiRVFJMpcrwjcVlh8A8QR7WribXOUdTxMh2crjRAQ";
