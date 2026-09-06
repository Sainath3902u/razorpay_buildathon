// "use client";

// import { ReactNode } from "react";
// import { X } from "lucide-react";

// interface ModalProps {
//   open: boolean;
//   title?: string;
//   onClose: () => void;
//   children: ReactNode;
// }

// export function Modal({
//   open,
//   title,
//   onClose,
//   children,
// }: ModalProps) {
//   if (!open) {
//     return null;
//   }

//   return (
//     <div
//       className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4"
//       onMouseDown={(event) => {
//         if (event.target === event.currentTarget) {
//           onClose();
//         }
//       }}
//     >
//       <div className="relative max-h-[90vh] w-full max-w-3xl overflow-hidden rounded-2xl bg-white shadow-2xl">

//         {/* Header */}
//         <div className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">

//           {title ? (
//             <h2 className="text-lg font-semibold text-slate-950">
//               {title}
//             </h2>
//           ) : (
//             <div />
//           )}

//           <button
//             type="button"
//             aria-label="Close modal"
//             onClick={onClose}
//             className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
//           >
//             <X className="h-5 w-5" />
//           </button>

//         </div>

//         {/* Content */}
//         <div className="max-h-[calc(90vh-73px)] overflow-y-auto p-6">
//           {children}
//         </div>

//       </div>
//     </div>
//   );
// }


"use client";

import { ReactNode } from "react";
import { X } from "lucide-react";

interface ModalProps {
  open: boolean;
  title?: string;
  onClose: () => void;
  children: ReactNode;

  /*
   * Allows the page to move/resize the modal
   * when the AI assistant is open.
   */
  className?: string;
}

export function Modal({
  open,
  title,
  onClose,
  children,
  className = "",
}: ModalProps) {
  if (!open) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) {
          onClose();
        }
      }}
    >
      <div
        className={`relative max-h-[90vh] w-full max-w-3xl overflow-hidden rounded-2xl bg-white shadow-2xl transition-all duration-300 ${className}`}
      >

        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">

          {title ? (
            <h2 className="text-lg font-semibold text-slate-950">
              {title}
            </h2>
          ) : (
            <div />
          )}

          <button
            type="button"
            aria-label="Close modal"
            onClick={onClose}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
          >
            <X className="h-5 w-5" />
          </button>

        </div>

        {/* Content */}
        <div className="max-h-[calc(90vh-73px)] overflow-y-auto p-6">
          {children}
        </div>

      </div>
    </div>
  );
}