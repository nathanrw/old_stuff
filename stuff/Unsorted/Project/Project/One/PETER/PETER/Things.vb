Module Things

    Public Function Multiliner(ByVal thestring, ByVal linelength)

        Dim newstring As String = ""
        Dim Numlines As Integer = Len(thestring) / linelength
        For Counter As Integer = 0 To Numlines - 1
            Try
                newstring = newstring + thestring.Substring(Counter * linelength, linelength)
            Catch
                newstring = newstring + thestring.Substring(Counter * linelength, (Len(thestring) Mod linelength))
            End Try
            newstring = newstring + vbCrLf
        Next
        Return newstring

    End Function

End Module
