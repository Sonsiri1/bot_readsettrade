"use client";
import { useRouter } from "next/navigation";
import Swal from "sweetalert2";
import React from "react";

const LogOutButton = () => {
  // const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const router = useRouter();
  const handleLogout = async () => {
    const result = await Swal.fire({
      title: "ออกจากระบบ?",
      text: "คุณต้องการออกจากระบบใช่ไหม",
      icon: "warning",
      showCancelButton: true,
      cancelButtonText: "ยกเลิก",
      confirmButtonText: "ยืนยัน",
      // cancelButtonColor: "#888780",
      // confirmButtonColor: "#00d4aa",
      buttonsStyling: false,
      allowOutsideClick: false,

      background: "#0a0e1a",
      color: "#fff",

      customClass: {
        popup: "!border-2 !border-[#00d4aa] bg-[#0a0e1a] rounded-xl",

        confirmButton:
          "bg-[#00d4aa]/90 hover:bg-[#00d4aa] text-black font-semibold px-5 py-2 rounded-lg shadow-lg transition cursor-pointer",

        cancelButton:
          "bg-zinc-800 hover:bg-zinc-700 text-zinc-300 px-5 py-2 rounded-lg border border-zinc-700 transition cursor-pointer mr-2",
      },

      reverseButtons: true
    });

    if (result.isConfirmed) {
      await fetch(`/api/logout`, {
        method: "POST",
        // credentials: "include",
      });

      await Swal.fire({
        title: "ออกจากระบบสำเร็จ",
        icon: "success",
        timer: 1500,
        showConfirmButton: false,
        iconColor: "#00d4aa",

        background: "#0a0e1a",
        color: "#fff",

        allowOutsideClick: false,
        allowEscapeKey: false,

        customClass: {
          popup:
            "!border-2 !border-[#00d4aa]/60 bg-[#0a0e1a] rounded-xl shadow-[0_0_20px_rgba(0,212,170,0.3)]",
          title: "text-white",
        },
      });
      
      router.push("/");
    }
  };

  return (
    <button onClick={handleLogout} className="rounded-xl items-center shadow-sm p-2 bg-[#00d4aa] hover:bg-[#00f0c0] text-[#0a0e1a] py-3.5 text-sm font-bold tracking-[0.15em] transition-all hover:-translate-y-0.5 active:translate-y-0 hover:shadow-2xl cursor-pointer">
      ออกจากระบบ
    </button>
  );
};

export default LogOutButton;
