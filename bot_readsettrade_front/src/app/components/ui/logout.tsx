"use client";
import { useRouter } from "next/navigation";
import Swal from "sweetalert2";
import React from "react";

const LogOutButton = () => {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const router = useRouter();
  const handleLogout = async () => {
    const result = await Swal.fire({
      title: "ออกจากระบบ?",
      text: "คุณต้องการออกจากระบบใช่ไหม",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "ใช่",
      cancelButtonText: "ยกเลิก",
      confirmButtonColor: "#0F6E56",
      cancelButtonColor: "#888780",
    });

    if (result.isConfirmed) {
      await fetch(`${API_URL}/api/logout`, {
        method: "POST",
        credentials: "include",
      });

      await Swal.fire({
        title: "ออกจากระบบสำเร็จ",
        icon: "success",
        timer: 1500,
        showConfirmButton: false,
        iconColor: "#0F6E56",
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
