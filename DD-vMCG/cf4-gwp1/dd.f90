
        Program sbrain

        implicit none

        integer I1,I2,I3,I4,I5,I6,N1,N2,N3,P 
        integer T1,T2,T3,T4,T5,T6,natm
        real*8 J,O,OS,X(400,400,400),Y(400,400,400),norm
        real*8 rx1,ry1,rz1,rx2,ry2,rz2,r
        real*8 rmag,rpz,rmz,dr,rp1,rp2,rm1,rm2,rpy,rmy,rtot 
        real*8 RXMAX,RYMAX,RZMAX,DELX,DELY,DELZ,rpx,rmx
        character*79 string

! READ THE CUBE FILE AND SPLIT INTO rho+ and rho-
        open(2,file='ddtraj.pl',form='formatted')
     10 continue
        read(2,'(75a)') string
        if (string(16:16) .eq. '6') then
          write(*,*)  '5'
          write(*,*)  ' '
          write(*,*)  '6' ,string(35:70)
          read(2,'(75a)') string
          write(*,*) '9 ',string(35:70)
          read(2,'(75a)') string
          write(*,*) '9 ',string(35:70)
          read(2,'(75a)') string
          write(*,*) '9 ',string(35:70)
          read(2,'(75a)') string
          write(*,*) '9 ',string(35:70)
          go to 10
        else 
           go to 10
        endif

        end
